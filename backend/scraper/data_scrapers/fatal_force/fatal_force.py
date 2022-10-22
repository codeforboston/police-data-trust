import pandas as pd
from client import FF_Client
from collections import namedtuple
import backend.database as md
from backend.scraper.data_scrapers.scraper_utils import create_bulk, map_cols, map_df, drop_existing_records

# extract csv from URL and convert to dataframe
def get_data():
    dataset = FF_Client()
    r = dataset.run()
    temp_csv = 'temp.csv'
    open(temp_csv, 'wb').write(r.content)
    df = pd.read_csv(temp_csv, dtype={"id": str}, index_col=None)
    return df

# map data in csv to columns contained in models
def fatal_cols():
    dataset = map_cols(get_data(), 
    {
        "id": "source_id",
        "name": "victim_name",
        "gender": "victim_gender",
        "race": "victim_race",
        "age": "victim_age",
        "manner_of_death": "manner_of_injury",
        "date": "incident_date",
        "city": "city",
        "state": "state",
        "latitude": "latitude",
        "longitude": "longitude"
    },
    ).set_index("source_id", drop=False)
    print(dataset)
    dataset = dataset[~dataset.index.duplicated(keep='first')]
    dataset = drop_existing_records(dataset, "fatal_force")
    return dataset


def create_FF_orm(r: namedtuple):
    victim = md.Victim(
        name=r.victim_name,
        race=r.victim_race,
        gender=r.victim_gender,
        deceased=True,
    )

    incident = md.Incident(
        source="fatal_force",
        source_id=r.source_id, 
        time_of_incident=r.incident_date,
        description=r.manner_of_injury,
        complaint_date=r.incident_date,
        latitude=r.latitude,
        longitude=r.longitude,
        victims=[victim],
        
    )
    
    return incident

def create_source():
    source = md.Source(
        id = 'fatal_force',
        publication_name = 'Fatal Force',
        publication_date = '05/22/2022',
        author = 'test',
        URL = 'https://github.com/washingtonpost/data-police-shootings/releases/download/v0.1/fatal-police-shootings-data.csv'
    )
    return source


def create_incidents(data):
    incidents = map_df(data, create_FF_orm)
    return incidents


def append_to_index(incidents):
    create_bulk(incidents)