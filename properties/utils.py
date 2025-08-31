from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.

    Returns:
        dict: {
            "hits": int,
            "misses": int,
            "hit_ratio": float
        }
    """
    try:
        # Connect to Redis via django-redis
        redis_conn = get_redis_connection("default")

        # Get Redis INFO stats
        info = redis_conn.info("stats")

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        total = hits + misses
        hit_ratio = (hits / total) if total > 0 else 0.0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 4),  # rounded for readability
        }

        # Log the metrics
        logger.info(f"Redis Cache Metrics: {metrics}")

        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {"hits": 0, "misses": 0, "hit_ratio": 0.0}


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

