from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model to support different roles.
    """
    ROLE_OVERALL_ADMIN = 'overall_admin'
    ROLE_SECTOR_ADMIN = 'sector_admin'
    ROLE_SERVICE_PROVIDER = 'service_provider'
    ROLE_CLIENT = 'client'

    ROLE_CHOICES = (
        (ROLE_OVERALL_ADMIN, 'Overall Admin'),
        (ROLE_SECTOR_ADMIN, 'Sector Admin'),
        (ROLE_SERVICE_PROVIDER, 'Service Provider'),
        (ROLE_CLIENT, 'Client'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, db_index=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
