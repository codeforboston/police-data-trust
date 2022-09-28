import math
from itertools import zip_longest
from typing import List
from collections import namedtuple
import backend.database as md
from backend.database import db
from backend.api import create_app

app = create_app("development")


def map_cols(df, m: dict):
    return df[list(m.keys())].rename(columns=m)


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
        md.Officer(last_name=name, race=race)
        for name, race in zip_longest(names, races)
    ]


def parse_accusations(r: namedtuple, officers: List[md.Officer]):
    outcomes = parse_parts(r.officer_outcomes)
    return [
        md.Accusation(outcome=outcome, officer=officer)
        for officer, outcome in zip_longest(officers, outcomes)
    ]


def create_orm(r: namedtuple, source):
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


def create_bulk(instances, chunk_size=1000):
    """Inserts ORM instances into the database"""
    with app.app_context():
        for chunk in range(0, len(instances), chunk_size):
            db.session.add_all(instances[chunk : chunk + chunk_size])
            db.session.flush()
        db.session.commit()


def insert_model(instance):
    with app.app_context():
        db.session.merge(instance)
        db.session.commit()


def drop_existing_records(dataset, source):
    with app.app_context():
        existing_source_ids = list(
            s
            for (s,) in db.session.query(md.Incident.source_id).filter(
                md.Incident.source == source, md.Incident.source_id is not None
            )
        )
    return dataset.drop(existing_source_ids)
