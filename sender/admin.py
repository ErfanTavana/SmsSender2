from django.contrib import admin
from .models import SmsProgram, UserTask


@admin.register(SmsProgram)
class SmsProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'message', 'organization', 'created_at')
    list_filter = ('organization', 'created_at')
    search_fields = ('name', 'message__content', 'organization__name')
    filter_horizontal = ('groups', 'users')
    ordering = ('-created_at',)


@admin.register(UserTask)
class UserTaskAdmin(admin.ModelAdmin):
    list_display = ('sms_program', 'organization', 'assigned_user', 'created_at')
    list_filter = ('organization', 'created_at')
    search_fields = ('sms_program__name', 'organization__name', 'assigned_user__username')
    filter_horizontal = ('contacts',)
    ordering = ('-created_at',)
