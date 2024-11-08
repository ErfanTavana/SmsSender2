from django.contrib import admin
from .models import User
from organizations.models import Group

class UserAdmin(admin.ModelAdmin):
    # Existing configurations...

    fieldsets = (
        (None, {
            'fields': ('phone_number', 'first_name', 'last_name', 'gender', 'password', 'organization')
        }),
        ('Permissions', {
            'fields': (
                'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',
                'can_access_messages', 'can_access_users', 'can_access_groups',
                'can_access_sms_program', 'can_access_contacts', 'can_send_bulk_sms',
                'can_add_contacts'  # Add the new permission field here
            )
        }),
        ('Important dates', {
            'fields': ('date_joined',),
        }),
    )

# Register the updated User model with the custom UserAdmin
admin.site.register(User, UserAdmin)
