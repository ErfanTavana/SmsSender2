from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()

class Message(models.Model):
    """
    Model to represent messages.
    """
    MESSAGE_TYPE_CHOICES = [
        ('همگانی', 'همگانی'),
        ('فردی', 'فردی'),
    ]

    text = models.TextField(verbose_name="متن پیام")
    organization = models.ForeignKey("organizations.Organization", on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name="سازمان")

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ایجاد کننده")
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, verbose_name="نوع ارسال پیام")
    is_approved = models.BooleanField(default=False, verbose_name="آیا پیام تایید شده است؟")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return f"پیام از {self.created_by} - {self.text[:20]}"

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام‌ها'
