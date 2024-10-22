from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid


class CustomUserManager(BaseUserManager):
    """
    Custom user manager to handle user creation with phone number and user type.
    """
    is_superuser = models.BooleanField(
        default=False,
        help_text='Designates that this user has all permissions without explicitly assigning them.'
    )
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='user_set'  # Related name for reverse lookup
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='user_set'  # Related name for reverse lookup
    )
    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a User with the given phone number, user type, and password.
        """
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given phone number, user type, and password.
        """
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
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site."
    )  # Determines if the user can access the admin site
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        )
    )  # Indicates if the user account is active
    date_joined = models.DateTimeField("date joined", default=timezone.now)  # Timestamp when the user joined

    USERNAME_FIELD = 'phone_number'  # Set phone_number as the unique identifier for authentication

    objects = CustomUserManager()  # Assign the custom user manager

    def save(self, *args, **kwargs):
        """
        Override the save method to generate a unique ID and update phone fields before saving.
        """
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Return the string representation of the user, which is the phone number.
        """
        return f'{self.phone_number} - {self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربرها'
