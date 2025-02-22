from django.db import models
from accounts.models import User

class Sector(models.Model):
    """
    Represents a major economic sector (e.g., 'Legal Services', 'Healthcare').
    """
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='sector_thumbnails/', blank=True, null=True)
    admins = models.ManyToManyField(
        User, 
        related_name='sectors', 
        limit_choices_to={'role': User.Role.SECTOR_ADMIN},
        blank=True  
    )

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """
    Represents a subcategory within a sector (e.g., 'Family Lawyer' under 'Legal Services').
    """
    sector = models.ForeignKey(Sector, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='subcategory_thumbnails/', blank=True, null=True)

    class Meta:
        unique_together = ('sector', 'name')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.sector.name})"


class ProviderProfile(models.Model):
    """
    Represents a service provider's profile.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': User.Role.SERVICE_PROVIDER}
    )
    business_name = models.CharField(max_length=255, blank=True, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT, db_index=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, db_index=True)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    subcounty = models.CharField(max_length=100, blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)
    verification_document = models.FileField(upload_to='verification_docs/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    recommended_providers = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return self.business_name or self.user.get_full_name() or self.user.username


class PortfolioImage(models.Model):
    """
    Represents images uploaded by service providers to showcase their work.
    """
    provider = models.ForeignKey(ProviderProfile, related_name='portfolio_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='portfolio_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Portfolio Image for {self.provider.business_name or self.provider.user.username}"


class Review(models.Model):
    """
    Represents a client review for a service provider.
    """
    provider = models.ForeignKey(ProviderProfile, related_name='reviews', on_delete=models.CASCADE)
    client = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'role': User.Role.CLIENT}
    )
    rating = models.PositiveSmallIntegerField(db_index=True)  # 1-5 rating scale
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review ({self.rating}/5) by {self.client.username} on {self.provider}"
