from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'gender', 'organization', 'created_by')
    search_fields = ('first_name', 'last_name', 'phone_number', 'organization__name')
    list_filter = ('gender', 'organization', 'groups')
    ordering = ('-first_name',)
    fields = ('first_name', 'last_name', 'phone_number', 'gender', 'created_by', 'organization', 'groups')

    filter_horizontal = ('groups',)
