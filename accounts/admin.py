from django.contrib import admin
from .models import User



class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'first_name', 'last_name', 'gender', 'is_staff', 'is_active', 'date_joined', 'organization')
    search_fields = ('phone_number', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'gender')  # اضافه کردن فیلتر جنسیت
    ordering = ('-date_joined',)
    readonly_fields = ('id', 'date_joined')

    fieldsets = (
        (None, {
            'fields': ('phone_number', 'first_name', 'last_name', 'gender', 'password', 'organization')  # اضافه کردن فیلد سازمان
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('date_joined',),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # اگر شیء وجود دارد، برخی فیلدها را فقط خواندنی کنید
            return self.readonly_fields + ('password',)
        return self.readonly_fields

# Register the User model with the custom UserAdmin
admin.site.register(User, UserAdmin)