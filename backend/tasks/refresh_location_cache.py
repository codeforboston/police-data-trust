from backend.api import create_app
from backend.services.location_cache_service import LocationCacheService


def main() -> None:
    app = create_app()
    with app.app_context():
        result = LocationCacheService().refresh_location_richness_cache()
        print(result)


if __name__ == "__main__":
    main()
