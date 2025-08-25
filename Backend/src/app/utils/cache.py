from functools import lru_cache
from geopy.geocoders import Nominatim

# Simple geocoder with caching (same behavior as your original)
_geolocator = Nominatim(user_agent="trip-location-tester")

@lru_cache(maxsize=1000)
def cached_reverse_geocode(lat, lon):
    try:
        loc = _geolocator.reverse((lat, lon), language="en", timeout=10)
        return loc.address if loc else "Unknown location"
    except Exception:
        return "Geocoding error"
