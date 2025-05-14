from django.contrib import admin
from .models import Device, DeviceLog

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("uid", "name", "location", "description")
    search_fields = ("uid", "name", "location")
    list_filter = ("location",)
    ordering = ("uid",)

@admin.register(DeviceLog)
class DeviceLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "device", "level", "message_short", "module", "code")
    search_fields = ("message", "module", "device__uid", "device__name")
    list_filter = ("level", "module", "timestamp")
    ordering = ("-timestamp",)
    readonly_fields = ("timestamp",)

    def message_short(self, obj):
        return (obj.message[:60] + "...") if len(obj.message) > 60 else obj.message
    message_short.short_description = "Message"
