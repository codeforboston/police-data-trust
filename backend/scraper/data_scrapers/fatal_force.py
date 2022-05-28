import os
if os.getcwd().endswith("scraper"):
    # Run this notebook from the repo root
    os.chdir("../..")
import sys
import math
import datetime
import numpy as np
import pandas as pd
import sqlalchemy
import psycopg2
from itertools import zip_longest
from typing import List
import requests
from IPython.display import display, HTML
from collections import namedtuple
from backend.database import db, Incident, Officer, Accusation, Victim

url = 'https://github.com/washingtonpost/data-police-shootings/releases/download/v0.1/fatal-police-shootings-data.csv'

df = pd.read_csv(url)

def map_cols(df, m: dict):
    return df[list(m.keys())].rename(columns=m)

def cols():
    data = pd.read_csv(url, dtype={"id": str})
    dataset = map_cols(data, 
    {
        "id": "source_id",
        "name": "victim_name",
        "gender": "victim_gender",
        "race": "victim_race",
        "age": "victim_age",
        "manner of death": "manner_of_injury",
        "date": "incident_date",
        "city": "city",
        "state": "state",
    },
    ).set_index("source_id", drop=False)


    print(dataset.columns)
    print(dataset.dtypes)

def create_bulk(instances, chunk_size=1000):
    """Inserts ORM instances into the database"""
    with app.app_context():
        for chunk in range(0, len(instances), chunk_size):
            db.session.add_all(instances[chunk : chunk + chunk_size])
            db.session.flush()
        db.session.commit()


def isnan(x):
    return isinstance(x, float) and math.isnan(x)


def nan_to_none(x):
    return None if isnan(x) else x


def strip_nan(r):
    return r._make([nan_to_none(e) for e in r])


def map_df(df, mapper):
    return [mapper(strip_nan(r)) for r in df.itertuples(index=False)]


def parse_int(value):
    try:
        return int(value)
    except ValueError:
        return None


def location(r: namedtuple):
    return " ".join(filter(None, [r.address, r.city, r.state, r.zip]))


def parse_parts(s: str):
    return list(map(lambda x: x.strip(), s.split(","))) if s else []


def parse_officers(r: namedtuple):
    names = parse_parts(r.officer_names_draft)
    races = parse_parts(r.officer_races_draft)

    return [
        Officer(last_name=name, race=race)
        for name, race in zip_longest(names, races)
    ]


def parse_accusations(r: namedtuple, officers: List[Officer]):
    outcomes = parse_parts(r.officer_outcomes)
    return [
        Accusation(outcome=outcome, officer=officer)
        for officer, outcome in zip_longest(officers, outcomes)
    ]


def create_orm(r: namedtuple):
    victim = Victim(
        name=r.victim_name,
        race=r.victim_race,
        gender=r.victim_gender,
        manner_of_injury=r.manner_of_injury,
        deceased=True,
    )
    officers = parse_officers(r)
    accusations = parse_accusations(r, officers)
    incident = Incident(
        source_id=r.source_id,
        source="fatal",
        time_of_incident=r.incident_date,
        location=location(r),
        description=r.description,
        department=r.department,
        latitude=r.latitude,
        longitude=r.longitude,
        victims=[victim],
        officers=officers,
        accusations=accusations,
    )
    return incident