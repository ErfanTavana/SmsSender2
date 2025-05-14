from django.db import models


class Device(models.Model):
    uid = models.CharField(max_length=100, unique=True)  # مثل MAC یا UUID
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
    module = models.CharField(max_length=100, blank=True, null=True)  # مثل sms_sender_thread
    code = models.IntegerField(blank=True, null=True)  # مثلاً کد خطا یا وضعیت
    extra_data = models.JSONField(blank=True, null=True)  # اطلاعات اضافی مثل حافظه، وضعیت صف، آی‌پی

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["device", "level"]),
        ]

    def __str__(self):
        return f"[{self.level}] {self.timestamp} - {self.device}"
