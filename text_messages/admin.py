
from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'text', 'organization' ,'created_by', 'message_type', 'is_approved', 'created_at' , 'groups'
    )
    search_fields = ('text', 'created_by__username', 'organization__name')
    list_filter = ('message_type', 'is_approved', 'organization')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('text', 'organization', 'created_by', 'message_type', 'is_approved', 'created_at','groups')
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # می‌توانید اینجا بر اساس سازمان کاربر، داده‌ها را فیلتر کنید (در صورت نیاز)
        return qs

# ثبت مدل پیام در پنل ادمین
admin.site.register(Message, MessageAdmin)
