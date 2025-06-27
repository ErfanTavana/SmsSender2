from io import StringIO
from django.contrib import admin
from import_export import resources, fields, widgets
from import_export.formats.base_formats import XLSX, CSV, JSON
from import_export.admin import ImportExportModelAdmin

from .models import Contact, Organization, Group
from .forms import ContactImportForm

import re
from import_export.results import RowResult


def normalize_phone_number(phone_number):
    """
    Normalize and validate Iranian phone numbers.
    Returns the phone number in standard format (09xxxxxxxxx).
    """
    phone_number = re.sub(r'\s+|-', '', phone_number)
    pattern = r'^(?:\+98|0098|98|0)?(9\d{9})$'

    if re.match(r'^(9\d{9})$', phone_number):
        return '0' + phone_number

    if re.match(r'^(09\d{9})$', phone_number):
        return phone_number

    elif re.match(pattern, phone_number):
        if phone_number.startswith('+98'):
            return '0' + phone_number[3:]
        elif phone_number.startswith('0098'):
            return '0' + phone_number[4:]
        elif phone_number.startswith('98'):
            return '0' + phone_number[2:]

    raise ValueError("شماره تلفن معتبر نیست. شماره تلفن باید یک شماره معتبر ایرانی باشد.")


class Txt:
    def get_title(self):
        return "TXT"

    def export_data(self, dataset, **kwargs):
        output = StringIO()
        for row in dataset.dict:
            output.write(f"{row['phone_number']}\n")
        return output.getvalue()

    def is_binary(self):
        return False

    def get_content_type(self):
        return "text/plain"

    def get_extension(self):
        return 'txt'


class ContactResource(resources.ModelResource):
    organization = fields.Field(
        column_name='organization_id',
        attribute='organization',
        widget=widgets.ForeignKeyWidget(Organization, 'id')
    )
    phone_number = fields.Field(
        column_name='phone_number',
        attribute='phone_number'
    )
    groups_ids = fields.Field(
        column_name='groups_ids',
        attribute=None
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = {}

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

    def before_import(self, dataset, using_transactions=None, dry_run=None, **kwargs):
        form_data = kwargs.get('form')
        self.context = {
            'update_name': form_data.cleaned_data.get('update_name') if form_data else False
        }
        print("✅ before_import - update_name =", self.context['update_name'])

        # حذف ردیف‌های خالی (صرفا لاگ می‌زند)
        empty_rows = []
        for i, row in enumerate(dataset.dict):
            phone = row.get('phone_number')
            org_id = row.get('organization_id')
            if (
                    not phone or str(phone).strip() in ["", "nan", "None"] or
                    not org_id or str(org_id).strip() in ["", "nan", "None"]
            ):
                empty_rows.append(i)

        if empty_rows:
            print(f"⚠️ {len(empty_rows)} ردیف ناقص پیدا شد و در import_row نادیده گرفته می‌شوند.")

    def get_instance(self, instance_loader, row):
        raw_phone = row.get('phone_number')
        org_id = row.get('organization_id')
        print("💡 get_instance - raw_phone =", raw_phone)
        print("💡 get_instance - org_id =", org_id)

        if not raw_phone or not org_id:
            return None

        normalized = normalize_phone_number(str(raw_phone))
        row['phone_number'] = normalized

        try:
            org = Organization.objects.get(id=org_id)
            print("✅ سازمان یافت شد:", org)
        except Organization.DoesNotExist:
            print(f"❌ سازمان با id={org_id} یافت نشد.")
            return None

        qs = Contact.objects.filter(phone_number=normalized, organization=org)
        if qs.exists():
            print("✅ رکورد موجود پیدا شد.")
            return qs.first()
        return None


    def import_row(self, row, instance_loader, **kwargs):
        raw_phone = row.get('phone_number')
        org_id = row.get('organization_id')

        if (
                not raw_phone or str(raw_phone).strip() in ["", "nan", "None"]
                or not org_id or str(org_id).strip() in ["", "nan", "None"]
        ):
            print(f"⚠️ ردیف ناقص رد شد: {row}")
            # ردیف Skip شود بدون خطا
            row_result = RowResult()
            row_result.import_type = RowResult.IMPORT_TYPE_SKIP
            return row_result

        try:
            normalized = normalize_phone_number(str(raw_phone))
            row['phone_number'] = normalized
        except Exception as e:
            print(f"❌ خطای اعتبارسنجی شماره تلفن: {e}")
            row_result = RowResult()
            row_result.import_type = RowResult.IMPORT_TYPE_SKIP
            return row_result

        instance = self.get_instance(instance_loader, row)
        existing_groups = set(instance.groups.all()) if instance else set()

        import_result = super().import_row(row, instance_loader, **kwargs)

        if import_result and import_result.object_id:
            db_instance = Contact.objects.get(pk=import_result.object_id)
            db_instance.phone_number = normalized

            update_name = self.context.get('update_name', False)
            if update_name:
                db_instance.first_name = row.get('first_name') or db_instance.first_name
                db_instance.last_name = row.get('last_name') or db_instance.last_name

            db_instance.save()

            group_ids = row.get('groups_ids')
            new_groups = set()
            if group_ids:
                clean_ids = [int(i.strip()) for i in str(group_ids).split(',') if i.strip().isdigit()]
                new_groups = set(Group.objects.filter(id__in=clean_ids))
                print("✅ گروه‌های جدید:", new_groups)
            else:
                print("ℹ️ گروهی برای این ردیف ثبت نشده.")

            combined_groups = existing_groups | new_groups
            db_instance.groups.set(combined_groups)

        return import_result

@admin.register(Contact)
class ContactAdmin(ImportExportModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'gender', 'organization', 'created_by')
    search_fields = ('first_name', 'last_name', 'phone_number', 'organization__name')
    list_filter = ('gender', 'organization', 'groups')
    ordering = ('-created_at',)
    fields = ('first_name', 'last_name', 'phone_number', 'gender', 'created_by', 'organization', 'groups')
    filter_horizontal = ('groups',)
    resource_class = ContactResource
    import_form_class = ContactImportForm

    def get_export_formats(self):
        formats = super().get_export_formats()
        return formats + [XLSX, CSV, JSON, Txt]
