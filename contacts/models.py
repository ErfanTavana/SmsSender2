from django.db import models
from organizations.models import Organization,Group
from django.contrib.auth import get_user_model

class Contact(models.Model):
    """
    Model to represent contacts.
    """
    GENDER_CHOICES = [
        ('مرد', 'مرد'),
        ('زن', 'زن'),
    ]

    first_name = models.CharField(max_length=150, verbose_name="نام")
    last_name = models.CharField(max_length=150, verbose_name="نام خانوادگی")
    phone_number = models.CharField(max_length=15, verbose_name="شماره تلفن همراه")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name="جنسیت")
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="کاربر ایجاد کننده")
    groups = models.ManyToManyField(Group, verbose_name="گروه‌ها", related_name="contacts")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="سازمان", related_name="contacts")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'مخاطب'
        verbose_name_plural = 'مخاطبین'
