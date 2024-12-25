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

class ContactResource(resources.ModelResource):
    class Meta:
        model = Contact
        fields = (
            'id', 'first_name', 'last_name', 'phone_number',
            'gender', 'created_by__phone_number', 'organization__name',
            'created_at'
        )
        export_order = (
            'id', 'first_name', 'last_name', 'phone_number',
            'gender', 'created_by__phone_number', 'organization__name',
            'created_at'
        )

@admin.register(Contact)
class ContactAdmin(ExportMixin, admin.ModelAdmin):
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
        # اضافه کردن فرمت‌های دیگر مانند TXT به فرمت‌ها
        return formats + [XLSX, CSV, JSON, Txt]  # اضافه کردن کلاس Txt به لیست فرمت‌ها (بدون پرانتز)
