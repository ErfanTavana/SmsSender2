from django.db import models
from datetime import timedelta
from django.utils import timezone

class Device(models.Model):
    uid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name or self.uid


class DeviceLog(models.Model):
    LEVEL_CHOICES = [
        ("DEBUG", "Debug"),
        ("INFO", "Info"),
        ("WARNING", "Warning"),
        ("ERROR", "Error"),
        ("CRITICAL", "Critical"),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    message = models.TextField()
    module = models.CharField(max_length=100, blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    extra_data = models.JSONField(blank=True, null=True)

    _last_cleanup_time = None  # کلاس-level متغیر برای کنترل تعداد پاکسازی‌ها

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["device", "level"]),
        ]

    def __str__(self):
        return f"[{self.level}] {self.timestamp} - {self.device}"

    def save(self, *args, **kwargs):
        now = timezone.now()

        # فقط اگر آخرین پاکسازی بیش از 5 دقیقه پیش انجام شده باشد
        if not DeviceLog._last_cleanup_time or (now - DeviceLog._last_cleanup_time) > timedelta(minutes=5):
            threshold = now - timedelta(hours=24)
            deleted_count, _ = DeviceLog.objects.filter(timestamp__lt=threshold).delete()

            print(f"[⏳ Cleanup] Deleted {deleted_count} old logs (older than 24h)")
            DeviceLog._last_cleanup_time = now

        super().save(*args, **kwargs)
