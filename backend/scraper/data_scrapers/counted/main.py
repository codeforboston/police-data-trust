
from pyrsistent import inc
from backend.scraper.data_scrapers.counted.counted import append_to_index, col_conv, create_incidents, extract_zip
from backend.scraper.data_scrapers.scraper_utils import drop_existing_records

extract_zip()
dataset = col_conv()
incidents = create_incidents(dataset)
append_to_index(incidents)
