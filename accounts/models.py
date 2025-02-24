from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    """
    Custom manager for User model with role handling.
    """
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set.")
        email = self.normalize_email(email)
        extra_fields.setdefault('role', User.Role.CLIENT)
        user = self.model(username=username, email=email, **extra_fields)
        if not password:
            raise ValueError("Password must be provided.")
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('role', User.Role.OVERALL_ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('role') != User.Role.OVERALL_ADMIN:
            raise ValueError("Superuser must have overall admin role.")
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    """
    Custom user model with role-based authentication.
    """
    class Role(models.TextChoices):
        OVERALL_ADMIN = 'overall_admin', 'Overall Admin'
        SECTOR_ADMIN = 'sector_admin', 'Sector Admin'
        SERVICE_PROVIDER = 'service_provider', 'Service Provider'
        CLIENT = 'client', 'Client'

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        db_index=True,
        default=Role.CLIENT
    )

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.get_role_display()}) - {self.email}"
