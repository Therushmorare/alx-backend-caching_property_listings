from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Fetches all Property objects with Redis caching.
    Cache key: 'all_properties'
    Expiry: 1 hour (3600 seconds)
    """
    properties = cache.get('all_properties')

    if properties is None:
        properties = Property.objects.all()
        # Cache the queryset for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)

    return properties

