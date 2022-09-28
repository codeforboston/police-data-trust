import glob
import os
import zipfile
import pandas as pd
from collections import namedtuple
import backend.database as md
from ..scraper_utils.utils import (
    create_bulk,
    map_cols,
    map_df,
    drop_existing_records,
)
from client import Counted_Client


data_dir = os.path.join(os.path.dirname(__file__), "scraper_data")


# extracts zipfile from Counted_Client function into cwd
def extract_zip():
    os.chdir(data_dir)
    curDir = os.getcwd()
    dataset = Counted_Client()
    r = dataset.run()
    open("thecounted-data.zip", "wb").write(r.content)
    zf = zipfile.ZipFile(curDir + "/thecounted-data.zip")
    zf.extractall(curDir)


# filters out any other filetype except .csv
def filter_csv():
    os.chdir(data_dir)
    curDir = os.getcwd()
    files = glob.glob(curDir + "/*.csv")
    return files


# creates dataframe and appends any other csv files
def append_dataframe(filtered_files):
    content = []
    for filename in filtered_files:
        df = pd.read_csv(filename, dtype={"uid": str}, index_col=None)
        content.append(df)
        counted_data = pd.concat(content)
    return counted_data


# Convert date to correct incident_date format
def convert_date(df):
    month_map = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }
    dates = pd.DataFrame(
        {
            "day": df.day,
            "month": df.month.apply(lambda x: month_map[x]),
            "year": df.year,
        }
    )
    converted_dates = pd.to_datetime(dates)
    df["incident_date"] = converted_dates
    print(df)
    return df


# Convert colummns name to map to schema
def col_conv():
    filtered_data = append_dataframe(filter_csv())
    df = convert_date(filtered_data)
    dataset = map_cols(
        df,
        {
            "uid": "source_id",
            "name": "victim_name",
            "gender": "victim_gender",
            "raceethnicity": "victim_race",
            "age": "victim_age",
            "incident_date": "incident_date",
            "streetaddress": "address",
            "city": "city",
            "state": "state",
            "lawenforcementagency": "department",
        },
    ).set_index("source_id", drop=False)
    dataset = dataset[~dataset.index.duplicated(keep="first")]
    dataset = drop_existing_records(dataset, "counted")
    return dataset


def create_counted_orm(r: namedtuple):
    victim = md.Victim(
        name=r.victim_name,
        race=r.victim_race,
        gender=r.victim_gender,
        deceased=True,
    )
    incident = md.Incident(
        source="counted",
        source_id=r.source_id,
        time_of_incident=r.incident_date,
        department=r.department,
        victims=[victim],
        location=f"{r.address} {r.city} {r.state}",
    )

    return incident


def create_source():
    source = md.Source(
        id="counted",
        publication_name="The Guardian",
        publication_date="06/1/2015",
        author="Jon Swaine, Oliver Laughland, Jamiles Lartey, Ciara McCarthy",
        URL="https://interactive.guim.co.uk/2015/\
        the-counted/thecounted-data.zip",
    )
    return source


def create_incidents(data):
    incidents = map_df(data, create_counted_orm)
    return incidents


def append_to_index(incidents):
    create_bulk(incidents)
