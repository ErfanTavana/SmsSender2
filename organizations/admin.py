from django.contrib import admin
from .models import Organization, Group


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'responsible_name', 'responsible_phone', 'created_at')
    search_fields = ('name', 'responsible_name')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    fields = ('name', 'responsible_name', 'responsible_phone', 'national_id', 'description')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'created_at')
    search_fields = ('name', 'organization__name')
    list_filter = ('organization', 'created_at')
    ordering = ('-created_at',)
    fields = ('name', 'organization', 'description')

