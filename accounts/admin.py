from django import forms
from django.contrib import admin
from .models import User


class UserAdminForm(forms.ModelForm):
    change_password = forms.BooleanField(required=False, initial=False, label="Change Password")

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        password = self.cleaned_data.get("password")
        change_password = self.cleaned_data.get("change_password")

        if change_password and password:
            user = self.instance  # گرفتن نمونه‌ی موجود کاربر
            if user.pk:  # اگر کاربر وجود داشته باشد
                user.set_password(password)
                return user.password  # بازگشت رمز عبور هش شده
        return self.instance.password  # حفظ رمز عبور قبلی


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm  # استفاده از فرم سفارشی
    fieldsets = (
        (None, {
            'fields': (
            'phone_number', 'first_name', 'last_name', 'gender', 'password', 'change_password', 'organization')
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