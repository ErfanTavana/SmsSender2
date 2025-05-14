from django.contrib import admin
from django.utils.html import format_html
from .models import Device, DeviceLog


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'location', 'description')
    search_fields = ('uid', 'name', 'location')
    ordering = ('uid',)


@admin.register(DeviceLog)
class DeviceLogAdmin(admin.ModelAdmin):
    list_display = ('colored_level', 'timestamp', 'device', 'short_message', 'module', 'code')
    list_filter = ('level', 'device', 'module')
    search_fields = ('message', 'module', 'device__uid')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)
    list_per_page = 50

    def short_message(self, obj):
        return (obj.message[:75] + '...') if len(obj.message) > 75 else obj.message
    short_message.short_description = "Message"

    def colored_level(self, obj):
        color_map = {
            'DEBUG': 'gray',
            'INFO': 'blue',
            'WARNING': 'orange',
            'ERROR': 'red',
            'CRITICAL': 'darkred',
        }
        return format_html(
            '<strong style="color:{}">{}</strong>',
            color_map.get(obj.level, 'black'),
            obj.level
        )
    colored_level.short_description = 'Level'

    # نمایش زیبای JSON
    def extra_data_pretty(self, obj):
        import json
        return format_html('<pre>{}</pre>', json.dumps(obj.extra_data, indent=2, ensure_ascii=False)) if obj.extra_data else "-"
    extra_data_pretty.short_description = "Extra Data"
