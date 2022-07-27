import pandas as pd
from client import FF_Client
from collections import namedtuple
import backend.database as md
from ..scraper_utils import create_bulk, map_cols, map_df, drop_existing_records


def get_data():
    dataset = FF_Client()
    r = dataset.run()
    df = pd.read_csv(r.content, dtype={"uid": str}, index_col=None)
    breakpoint()
    return df


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
    },
    ).set_index("source_id", drop=False)
    dataset = dataset[~dataset.index.duplicated(keep='first')]
    dataset = drop_existing_records(dataset, 'fatal_force')
    return dataset


def create_FF_orm(r: namedtuple, source):
    victim = md.Victim(
        name=r.victim_name,
        race=r.victim_race,
        gender=r.victim_gender,
        deceased=True,
    )
    officers = parse_officers(r)
    accusations = parse_accusations(r, officers)
    incident = md.Incident(
        source_id=r.source_id, 
        source=source,
        time_of_incident=r.incident_date,
        location=location(r),
        description=r.description,
        department=r.department,
        victims=[victim],
        officers=officers,
        accusations=accusations,
    )
    return incident
