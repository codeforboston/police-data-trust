from backend.api import create_app
from backend.services.agency_cache_service import AgencyCacheService


def main() -> None:
    app = create_app()
    with app.app_context():
        result = AgencyCacheService().refresh_agency_metrics_cache()
        print(result)


if __name__ == "__main__":
    main()
