from django.db.models.signals import pre_save
from django.dispatch import receiver
from geopy.geocoders import Nominatim
from .models import ProviderProfile

@receiver(pre_save, sender=ProviderProfile)
def geocode_location(sender, instance, **kwargs):
    if instance.address and not instance.location:
        try:
            geolocator = Nominatim(user_agent="service_marketplace")
            location = geolocator.geocode(instance.address)
            if location:
                instance.location = f"POINT({location.longitude} {location.latitude})"
        except Exception as e:
            print(f"Geocoding error: {str(e)}")