from io import StringIO
from django.contrib import admin
from import_export.admin import ExportMixin
from import_export.formats.base_formats import XLSX, CSV, JSON
from import_export import resources
from .models import Contact

# تعریف فرمت TXT
class Txt:
    """
    کلاس برای ایجاد خروجی به فرمت تکست.
    """
    def get_title(self):
        return "TXT"  # عنوان برای نمایش در لیست فرمت‌ها

    def export_data(self, dataset, **kwargs):
        """
        داده‌ها را به فرمت تکست (txt) تبدیل می‌کند.
        """
        output = StringIO()
        for row in dataset.dict:
            # فقط شماره تماس‌ها را استخراج می‌کنیم
            output.write(f"{row['phone_number']}\n")
        return output.getvalue()

    def is_binary(self):
        """
        متد is_binary برای فرمت تکست، که در اینجا False باز می‌گرداند،
        چون داده‌ها به‌صورت متنی هستند.
        """
        return False

    def get_content_type(self):
        """
        متد get_content_type برای تعیین نوع محتوای فایل TXT
        که به صورت text/plain خواهد بود.
        """
        return "text/plain"

    def get_extension(self):
        """
        متد get_extension برای برگرداندن پسوند مناسب فایل TXT
        """
        return 'txt'
from import_export import resources, fields, widgets
from .models import Contact, Organization, Group
from django.db.models import Q
import re

import re

def normalize_phone_number(phone_number):
    """
    Normalize and validate Iranian phone numbers.
    Returns the phone number in standard format (e.g., 09xxxxxxxxx).
    """
    phone_number = re.sub(r'\s+|-', '', phone_number)
    pattern = r'^(?:\+98|0098|98|0)?(9\d{9})$'

    # اگر شماره به صورت 10 رقمی باشد و با 9 شروع شود
    if re.match(r'^(9\d{9})$', phone_number):
        return '0' + phone_number

    # اگر شماره از قبل استاندارد باشد
    if re.match(r'^(09\d{9})$', phone_number):
        return phone_number

    # فرمت‌های بین‌المللی
    elif re.match(pattern, phone_number):
        if phone_number.startswith('+98'):
            return '0' + phone_number[3:]
        elif phone_number.startswith('0098'):
            return '0' + phone_number[4:]
        elif phone_number.startswith('98'):
            return '0' + phone_number[2:]

    raise ValueError("شماره تلفن معتبر نیست. شماره تلفن باید یک شماره معتبر ایرانی باشد.")


class ContactResource(resources.ModelResource):
    organization = fields.Field(
        column_name='organization',
        attribute='organization',
        widget=widgets.ForeignKeyWidget(Organization, 'name')
    )
    groups_ids = fields.Field(
        column_name='groups_ids',
        attribute=None
    )

    class Meta:
        model = Contact
        fields = (
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'gender',
            'created_by__phone_number',
            'organization',
            'created_at',
            'groups_ids',
        )
        export_order = fields

    def get_instance(self, instance_loader, row):
        raw_phone = row.get('phone_number')
        org_name = row.get('organization')
        normalized = None
        if raw_phone and org_name:
            try:
                normalized = normalize_phone_number(str(raw_phone))
                row['phone_number'] = normalized
            except Exception as e:
                raise ValueError(f"شماره تلفن '{raw_phone}' معتبر نیست: {e}")

            try:
                org = Organization.objects.get(name=org_name)
            except Organization.DoesNotExist:
                return None

            qs = Contact.objects.filter(phone_number=normalized, organization=org)
            if qs.exists():
                return qs.first()
        return None

    def import_row(self, row, instance_loader, **kwargs):
        raw_phone = row.get('phone_number')
        normalized = None
        if raw_phone:
            try:
                normalized = normalize_phone_number(str(raw_phone))
                row['phone_number'] = normalized
            except Exception as e:
                raise ValueError(f"شماره تلفن '{raw_phone}' معتبر نیست: {e}")

        instance = self.get_instance(instance_loader, row)
        if instance:
            existing_groups = set(instance.groups.all())
        else:
            existing_groups = set()

        import_result = super().import_row(row, instance_loader, **kwargs)

        if import_result.object_id:
            db_instance = Contact.objects.get(pk=import_result.object_id)

            # فقط اگر نرمال‌سازی شده بود
            if normalized:
                db_instance.phone_number = normalized
                db_instance.save()

            group_ids = row.get('groups_ids')
            if group_ids:
                clean_ids = [int(i.strip()) for i in str(group_ids).split(',') if i.strip().isdigit()]
                found_groups = list(Group.objects.filter(id__in=clean_ids))
                new_groups = set(found_groups)
            else:
                new_groups = set()

            combined_groups = existing_groups | new_groups
            db_instance.groups.set(combined_groups)

        return import_result


from import_export.admin import ImportExportModelAdmin

@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'gender', 'organization', 'created_by')
    search_fields = ('first_name', 'last_name', 'phone_number', 'organization__name')
    list_filter = ('gender', 'organization', 'groups')
    ordering = ('-created_at',)
    fields = ('first_name', 'last_name', 'phone_number', 'gender', 'created_by', 'organization', 'groups')
    filter_horizontal = ('groups',)
    resource_class = ContactResource

    def get_export_formats(self):
        """اضافه کردن فرمت‌های مختلف به گزینه‌ها."""
        formats = super().get_export_formats()
        return formats + [XLSX, CSV, JSON, Txt]