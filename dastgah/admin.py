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
    list_display = (
        'colored_level', 'timestamp', 'device', 'short_message', 'module', 'code', 'extra_data_summary'
    )
    list_filter = ('level', 'device', 'module')
    search_fields = ('message', 'module', 'device__uid', 'code')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp', 'extra_data_pretty')
    list_per_page = 50
    date_hierarchy = 'timestamp'

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

    def extra_data_pretty(self, obj):
        import json
        return format_html('<pre>{}</pre>', json.dumps(obj.extra_data, indent=2, ensure_ascii=False)) if obj.extra_data else "-"
    extra_data_pretty.short_description = "Extra Data (Pretty)"

    def extra_data_summary(self, obj):
        if not obj.extra_data:
            return "-"
        return ', '.join(f'{k}: {v}' for k, v in list(obj.extra_data.items())[:2])
    extra_data_summary.short_description = "Extra"
