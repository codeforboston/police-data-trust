import glob
import os
import sys
import zipfile
import pandas as pd
from collections import namedtuple
import backend.database as md
from ..scraper_utils import create_bulk, map_cols, map_df, drop_existing_records
from .client import *

data_dir = os.path.join(os.path.dirname(__file__), 'scraper_data')

#extracts zipfile from Counted_Client function into cwd
def extract_zip():
    os.chdir(data_dir)
    curDir = os.getcwd()
    dataset = Counted_Client()
    r = dataset.run()
    open('thecounted-data.zip', 'wb').write(r.content)
    zf = zipfile.ZipFile(curDir + '/thecounted-data.zip')
    zf.extractall(curDir)

#filters out any other filetype except .csv
def filter_csv():
    os.chdir(data_dir)
    curDir = os.getcwd()
    files = glob.glob(curDir + "/*.csv")
    return files

#creates dataframe and appends any other csv files
def append_dataframe(filtered_files):
    content = []
    for filename in filtered_files:
        df = pd.read_csv(filename, dtype={"uid": str}, index_col=None)
        content.append(df)
        counted_data = pd.concat(content)
    return counted_data
    
#convert colummns name to map to schema
def col_conv():
    df = append_dataframe(filter_csv())
    dataset = map_cols(df, {
        "uid": "source_id",
        "name": "victim_name",
        "gender": "victim_gender",
        "raceethnicity": "victim_race",
        "age": "victim_age",
        #"Date of Incident (month/day/year)": "incident_date",
        "streetaddress": "address",
        "city": "city",
        "state": "state",
        "lawenforcementagency":"department"
     
    },).set_index("source_id", drop=False)
    dataset = dataset[~dataset.index.duplicated(keep='first')]
    dataset = drop_existing_records(dataset, 'counted')
    return dataset

def create_counted_orm(r: namedtuple):
    victim = md.Victim(
        name=r.victim_name,
        race=r.victim_race,
        gender=r.victim_gender,
        deceased=True

    )
    incident = md.Incident(
        source='counted',
        source_id=r.source_id, 
        department=r.department,
        victims=[victim],
        location=f"{r.address} {r.city} {r.state}"
    )
    return incident
    
def create_incidents(data):
    incidents = map_df(data, create_counted_orm)
    return incidents

def append_to_index(incidents):
    create_bulk(incidents)
    
    #COLUMNS =
    # Index(['uid', 'name', 'age', 'gender', 'raceethnicity', 'month', 'day', 'year',
    #    'streetaddress', 'city', 'state', 'classification',
    #    'lawenforcementagency', 'armed'],
    #   dtype='object')
    







    