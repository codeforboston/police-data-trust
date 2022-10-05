from backend.scraper.data_scrapers.fatal_force.fatal_force import append_to_index, fatal_cols, create_incidents


dataset = fatal_cols()
incidents = create_incidents(dataset)
append_to_index(incidents)