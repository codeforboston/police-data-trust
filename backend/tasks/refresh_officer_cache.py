from backend.api import create_app
from backend.services.officer_cache_service import OfficerCacheService


def main() -> None:
    app = create_app()
    with app.app_context():
        result = OfficerCacheService().refresh_officer_metrics_cache()
        print(result)


if __name__ == "__main__":
    main()
