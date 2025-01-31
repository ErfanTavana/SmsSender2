from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid


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
    organization = models.ForeignKey('organizations.Organization', on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name="سازمان")
    groups = models.ManyToManyField("organizations.Group", verbose_name="گروه‌ها", related_name="users",
                                    blank=True)  # ارتباط با گروه‌ها
    jihadi_group = models.ForeignKey('JihadiGroup', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="گروه جهادی")

    # Access control fields
    can_access_messages = models.BooleanField("access to messages", default=False,
                                              help_text="Designates whether this user has access to messages.")
    can_access_users = models.BooleanField("access to users", default=False,
                                           help_text="Designates whether this user has access to manage users.")
    can_access_groups = models.BooleanField("access to groups", default=False,
                                            help_text="Designates whether this user has access to manage groups.")
    can_access_sms_program = models.BooleanField("access to SMS program", default=False,
                                                 help_text="Designates whether this user has access to SMS program.")
    can_access_contacts = models.BooleanField("access to contacts", default=False,
                                              help_text="Designates whether this user has access to manage contacts.")
    can_send_bulk_sms = models.BooleanField("send bulk SMS", default=False,
                                            help_text="Designates whether this user can send bulk SMS messages.")

    # New access control field for adding contacts through the app
    can_add_contacts = models.BooleanField(
        "add contacts through app",
        default=False,
        help_text="Designates whether this user can add contacts through the app."
    )
    USERNAME_FIELD = 'phone_number'  # Set phone_number as the unique identifier for authentication
    objects = CustomUserManager()  # Assign the custom user manager

    def __str__(self):
        return f'{self.phone_number} - {self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربرها'

class JihadiGroup(models.Model):
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="نام گروه جهادی"
    )
    leader_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="نام مسئول"
    )
    leader_national_id = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="کد ملی مسئول"
    )
    leader_contact_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="شماره تماس مسئول"
    )
    deputy_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="نام مسئول دوم"
    )
    deputy_contact_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="شماره تماس مسئول دوم"
    )
    service_province = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="استان محل خدمت"
    )
    service_city = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="شهرستان محل خدمت"
    )

    class Meta:
        verbose_name = "گروه جهادی"
        verbose_name_plural = "گروه‌های جهادی"

    def __str__(self):
        return self.name or "گروه جهادی بدون نام"
