from django.contrib import admin
from .models import User
from django import forms
from django.contrib.auth.hashers import make_password

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            return make_password(password)  # هش کردن رمز عبور
        return password

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm  # استفاده از فرم سفارشی
    fieldsets = (
        (None, {
            'fields': ('phone_number', 'first_name', 'last_name', 'gender', 'password', 'organization')
        }),
        ('Permissions', {
            'fields': (
                'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',
                'can_access_messages', 'can_access_users', 'can_access_groups',
                'can_access_sms_program', 'can_access_contacts', 'can_send_bulk_sms',
                'can_add_contacts'
            )
        }),
        ('Important dates', {
            'fields': ('date_joined',),
        }),
    )
    list_display = ('phone_number', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('phone_number', 'first_name', 'last_name')

# ثبت مدل User با تنظیمات سفارشی
admin.site.register(User, UserAdmin)
