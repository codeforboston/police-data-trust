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
from backend.api import create_app
app = create_app("development")

dataset_url = "https://docs.google.com/spreadsheets/d/1g7CNEDnjk5dH412wmVTAG6XtgWyS2Vax10-BbfsBp0U/export?format=csv"
dataset_path = "/Users/brianrennie/Documents/GitHub/police-data-trust/backend/scraper/MPV.csv"

def map_cols(df, m: dict):
    return df[list(m.keys())].rename(columns=m)

def cols():
    data = pd.read_csv(dataset_path, dtype={"Zipcode": str, "MPV ID": str}, skiprows=1)
    dataset = map_cols(data, 
    {
        "MPV ID": "source_id",
        "Victim's name": "victim_name",
        "Victim's gender": "victim_gender",
        "Victim's race": "victim_race",
        "Victim's age": "victim_age",
        "URL of image of victim": "victim_image_url",
        "Cause of death": "manner_of_injury",
        "Date of Incident (month/day/year)": "incident_date",
        "Street Address of Incident": "address",
        "City": "city",
        "State": "state",
        "Zipcode": "zip",
        "County": "county",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "A brief description of the circumstances surrounding the death": "description",
        "Official disposition of death (justified or other)": "officer_outcomes",
        "Agency responsible for death": "department",
        "Criminal Charges?": "criminal_charges",
        "Link to news article or photo of official document": "source_link",
        "Off-Duty Killing?": "off_duty_killing",
        "Encounter Type (DRAFT)": "encounter_type_draft",
        "Initial Reported Reason for Encounter (DRAFT)": "encounter_reason_draft",
        "Names of Officers Involved (DRAFT)": "officer_names_draft",
        "Race of Officers Involved (DRAFT)": "officer_races_draft",
        "Known Past Shootings of Officer(s) (DRAFT)": "officer_known_past_shootings_draft",
        "Call for Service? (DRAFT)": "call_for_service_draft",
    },
    ).set_index("source_id", drop=False)
     #Some rows are repeated, some ID's seem to be reused.
    dataset = dataset[~dataset.index.duplicated(keep='first')]
    assert not dataset.index.has_duplicates

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
        
breakpoint()

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
        source="mpv",
        time_of_incident=r.incident_date,
        location=location(r),
        description=r.description,
        department=r.department,
        # latitude=r.latitude,
        # longitude=r.longitude,
        victims=[victim],
        officers=officers,
        accusations=accusations,
    )
    return incident
