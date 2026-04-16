from backend.api import create_app
from backend.services.unit_cache_service import UnitCacheService


def main() -> None:
    app = create_app()
    with app.app_context():
        result = UnitCacheService().refresh_unit_metrics_cache()
        print(result)


if __name__ == "__main__":
    main()
