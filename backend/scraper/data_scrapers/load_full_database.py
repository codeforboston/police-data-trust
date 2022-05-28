import os
import math
import pandas as pd
from dateutil import parser

from ...api import db
from ...database import UseOfForce, Incident, Officer


def isnan(x):
    return isinstance(x, float) and math.isnan(x)


def nan_to_none(x):
    return None if isnan(x) else x


def parse_date(s):
    return parser.parse(s) if isinstance(s, str) and len(s) > 0 else None


def load_spreadsheet():
    pickle = os.path.join("excel_outputs", "full_database.pkl.zip")
    if os.path.exists(pickle):
        return pd.read_pickle(pickle)
    else:
        raise (
            f"No dataset found at {pickle}."
            + " Make sure to run the scraper first"
        )


def orm_location(row):
    fields = list(
        filter(
            None,
            [
                row.death_location_street_address,
                row.death_location_city,
                row.death_location_county,
                row.death_location_state,
            ],
        )
    )

    return None if len(fields) == 0 else " ".join(fields)


def row_to_orm(row):
    incident = Incident()
    row = row._make(map(nan_to_none, row))
    incident_date = parse_date(row.incident_date)
    incident_time = parse_date(row.incident_time)
    source = row.data_source_id
    use_of_force = row.death_manner
    location = orm_location(row)

    if location:
        incident.location = location
    if incident_date or incident_time:
        t = incident_date if incident_date else incident_time
        if incident_time:
            t = t.replace(
                hour=incident_time.hour,
                minute=incident_time.minute,
                second=incident_time.second,
            )
        incident.time_of_incident = t
    if row.department_present:
        incident.department = row.department_present
    if row.perpetrator:
        incident.officers = [
            Officer(
                last_name=row.perpetrator,
            )
        ]
    if row.description:
        incident.description = row.description
    if use_of_force:
        incident.use_of_force = [UseOfForce(item=use_of_force)]
    if source:
        incident.source = source

    return incident


def dataframe_to_orm(data):
    return [row_to_orm(row) for row in data.itertuples(index=False)]


def create_bulk(incidents, chunk_size=1000):
    for chunk in range(0, len(incidents), chunk_size):
        db.session.add_all(incidents[chunk : chunk + chunk_size])
        db.session.flush()
    db.session.commit()


def load_full_database():
    print("Loading incident dataset")
    data = load_spreadsheet()
    print("Converting dataset to ORM incidents")
    orm_incidents = dataframe_to_orm(data)
    print("Creating incidents in database")
    create_bulk(orm_incidents)
    print(f"Created {len(orm_incidents)} incident records")
