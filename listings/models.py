from django.db import models
from django.utils import timezone
from accounts.models import User
from django.contrib.gis.db.models import PointField 

# Core marketplace models

class Sector(models.Model):
    """
    Represents a major economic sector.
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
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """
    Represents a subcategory within a sector.
    """
    sector = models.ForeignKey(Sector, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='subcategory_thumbnails/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    location = PointField(geography=True, null=True, blank=True, srid=4326)  # <-- ADD THIS
    address = models.CharField(max_length=255, blank=True)  # <-- ADD THIS
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
    admin_verified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        limit_choices_to={'role': User.Role.SECTOR_ADMIN},
        related_name='verified_providers'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords for search optimization")
    is_featured = models.BooleanField(default=False, db_index=True)
    membership_tier = models.CharField(
        max_length=50, 
        choices=[('free', 'Free'), ('premium', 'Premium')],
        default='free'
    )
    recommended_providers = models.ManyToManyField('self', blank=True, symmetrical=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name or self.user.get_full_name() or self.user.username


class PortfolioImage(models.Model):
    """
    Represents images uploaded by service providers.
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
    rating = models.PositiveSmallIntegerField(db_index=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review ({self.rating}/5) by {self.client.username} on {self.provider}"


# Extended marketplace features

class Message(models.Model):
    """
    Represents a message exchanged between users.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"


class Booking(models.Model):
    """
    Represents a service booking request.
    """
    client = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': User.Role.CLIENT})
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE)
    service_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.client.username} with {self.provider}"


class Notification(models.Model):
    """
    Represents a notification for a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"


class Favorite(models.Model):
    """
    Represents a user's favorite provider.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'provider')

    def __str__(self):
        return f"{self.user.username} favorited {self.provider}"


class Report(models.Model):
    """
    Represents a report or complaint against a provider.
    """
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='reports')
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.reporter.username} on {self.provider}"
