from django.contrib import admin
from import_export.admin import ExportMixin
from import_export.formats.base_formats import XLSX, CSV, JSON
from import_export import resources
from .models import Contact

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
    ordering = ('-first_name',)
    fields = ('first_name', 'last_name', 'phone_number', 'gender', 'created_by', 'organization', 'groups')
    filter_horizontal = ('groups',)
    resource_class = ContactResource

    def get_export_formats(self):
        """اضافه کردن فرمت‌های مختلف به گزینه‌ها."""
        formats = super().get_export_formats()
        # اضافه کردن فرمت‌های دیگر مانند CSV و JSON
        return formats + [XLSX, CSV, JSON]  # بازگشت لیست فرمت‌ها شامل XLSX، CSV و JSON
