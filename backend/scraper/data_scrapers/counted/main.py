from backend.scraper.data_scrapers.counted.counted import (
    append_to_index,
    col_conv,
    create_incidents,
    extract_zip,
    create_source,
)
from backend.scraper.data_scrapers.scraper_utils.utils import insert_model


insert_model(create_source())
extract_zip()
dataset = col_conv()
incidents = create_incidents(dataset)
append_to_index(incidents)
