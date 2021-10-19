# Data Source Scraper

The `scrape_data_sources.py` script extracts incidents from external data sources. It should be able to run by itself, independent of the server and database.

## Setup

Follow the instructions [here](../../requirements/README.md) to install requirements.

## Usage

Run the scraper using `flask scrape` from the base of the repository.

You can also run the scraper in Docker:

```bash
# From the base of the repository
docker-compose build api
docker-compose run -u $(id -u) api flask scrape
# Stop the database service
docker-compose down
```

You may see several warnings about mixed types. The script could also take several minutes.

If the script finishes successfully, there should be an `excel_outputs/full_database.xlsx` file along with the raw data. This should hold all the data that the scraper was able to get. There should be four tabs: report, incident, victim, and death
