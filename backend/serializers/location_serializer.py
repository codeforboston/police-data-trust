
def serialize_location(location):
    if not location or not location.get("coords"):
        return None

    return {
        "latitude": location["coords"].y,
        "longitude": location["coords"].x,
        "city": location["city"],
        "state": location["state"],
    }
