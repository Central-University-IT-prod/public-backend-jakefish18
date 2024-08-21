from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="prod_olymp", timeout=3)


def get_address(address: str) -> str:
    """Validate user adress input by OSM."""
    return str(geolocator.geocode(address, language="ru"))


def get_place_by_address(address: str) -> str:
    """Retuning city of address."""
    return geolocator.geocode(address, language="ru").raw["name"]
