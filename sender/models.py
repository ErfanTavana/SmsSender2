# models.py
from django.db import models
from django.utils import timezone
from text_messages.models import Message
from accounts.models import User
from organizations.models import Organization, Group


class SmsProgram(models.Model):
    """
    Model to represent an SMS Program.
    """
    name = models.CharField(max_length=255, verbose_name="نام برنامه پیامکی")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="پیام مرتبط")
    organization = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="سازمان مرتبط")
    groups = models.ManyToManyField(Group, blank=True, verbose_name="گروه‌های هدف")
    users = models.ManyToManyField(User, blank=True, verbose_name="کاربران هدف")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'برنامه پیامکی'
        verbose_name_plural = 'برنامه‌های پیامکی'
