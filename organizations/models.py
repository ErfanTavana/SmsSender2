from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Organization(models.Model):
    """
    Model to represent organizations.
    """
    name = models.CharField(max_length=255, verbose_name="نام سازمان یا مجموعه")
    responsible_name = models.CharField(max_length=150, verbose_name="نام و نام خانوادگی مسئول", blank=True, null=True)
    responsible_phone = models.CharField(max_length=15, verbose_name="شماره تماس مسئول", blank=True, null=True)
    national_id = models.CharField(max_length=11, verbose_name="کد ملی مسئول", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد", blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات درباره سازمان یا مجموعه")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'سازمان'
        verbose_name_plural = 'سازمان‌ها'


class Group(models.Model):
    """
    Model to represent groups.
    """
    name = models.CharField(max_length=255, verbose_name="نام گروه")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="سازمان",
                                     related_name='groups')
    created_at = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ایجاد", blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات درباره گروه")
    sms_code = models.CharField(max_length=100, blank=True, null=True, verbose_name="کد پیامک")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'گروه'
        verbose_name_plural = 'گروه‌ها'
