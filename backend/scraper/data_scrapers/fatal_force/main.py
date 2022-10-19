from backend.scraper.data_scrapers.fatal_force.fatal_force import append_to_index, fatal_cols, create_incidents, create_source
from backend.scraper.data_scrapers.scraper_utils.utils import insert_model

insert_model(create_source())
dataset = fatal_cols()
incidents = create_incidents(dataset)
append_to_index(incidents)