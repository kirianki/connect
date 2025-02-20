from django.db import models
from accounts.models import User

class Sector(models.Model):
    """
    Represents a major economic sector (e.g., 'Legal Services', 'Healthcare').
    """
    name = models.CharField(max_length=100, unique=True)
    admins = models.ManyToManyField(User, related_name='sectors', limit_choices_to={'role': 'sector_admin'})

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """
    Represents a subcategory within a sector (e.g., 'Family Lawyer' under 'Legal Services').
    """
    sector = models.ForeignKey(Sector, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('sector', 'name')

    def __str__(self):
        return f"{self.sector.name} - {self.name}"


class ProviderProfile(models.Model):
    """
    Represents a service provider's profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'service_provider'})
    business_name = models.CharField(max_length=255, blank=True, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    verification_document = models.FileField(upload_to='verification_docs/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.business_name or self.user.get_full_name()


class Review(models.Model):
    """
    Represents a client review for a service provider.
    """
    provider = models.ForeignKey(ProviderProfile, related_name='reviews', on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'client'})
    rating = models.PositiveSmallIntegerField()  # 1-5 rating scale
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)  # Moderation flag

    def __str__(self):
        return f"Review by {self.client.username} on {self.provider}"
