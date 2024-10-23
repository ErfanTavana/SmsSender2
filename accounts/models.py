from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid
from organizations.models import Organization ,Group


class CustomUserManager(BaseUserManager):
    """
    Custom user manager to handle user creation with phone number and user type.
    """

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff') or not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_staff=True and is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that uses phone number for authentication and includes various user types.
    """
    phone_number = models.CharField(max_length=15, unique=True, default='', verbose_name="phone number")
    username = None  # Remove the username field as it's not needed
    email = None  # Remove the email field as it's not used
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField("first name", max_length=150, blank=True)  # User's first name
    last_name = models.CharField("last name", max_length=150, blank=True)  # User's last name
    gender = models.CharField(max_length=10, default='مرد', choices=[('مرد', 'مرد'), ('زن', 'زن')], blank=True,
                              verbose_name="جنسیت")  # Gender field
    is_staff = models.BooleanField("staff status", default=False,
                                   help_text="Designates whether the user can log into this admin site.")
    is_active = models.BooleanField("active", default=True,
                                    help_text="Designates whether this user should be treated as active.")
    date_joined = models.DateTimeField("date joined", default=timezone.now)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name="سازمان")
    groups = models.ManyToManyField(Group, verbose_name="گروه‌ها", related_name="users",
                                    blank=True)  # ارتباط با گروه‌ها

    USERNAME_FIELD = 'phone_number'  # Set phone_number as the unique identifier for authentication
    objects = CustomUserManager()  # Assign the custom user manager

    def __str__(self):
        return f'{self.phone_number} - {self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربرها'
