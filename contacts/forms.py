from import_export.forms import ImportForm
from django import forms

class ContactImportForm(ImportForm):
    update_name = forms.BooleanField(
        required=False,
        label="نام و نام خانوادگی بروزرسانی شود؟"
    )