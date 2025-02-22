from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model with role-based authentication.
    """
    class Role(models.TextChoices):
        OVERALL_ADMIN = 'overall_admin', 'Overall Admin'
        SECTOR_ADMIN = 'sector_admin', 'Sector Admin'
        SERVICE_PROVIDER = 'service_provider', 'Service Provider'
        CLIENT = 'client', 'Client'

    role = models.CharField(max_length=20, choices=Role.choices, db_index=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
