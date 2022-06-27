import glob
import os
import sys
import zipfile

import pandas as pd

from ..scraper_utils import create_bulk, create_orm, map_cols, map_df
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
     
    },).set_index("source_id", drop=False)
    dataset = dataset[~dataset.index.duplicated(keep='first')]
    print(dataset)
    return dataset

def create_incidents(data):
    incidents = map_df(data, create_orm)
    return incidents

def append_to_index(incidents):
    create_bulk(incidents)

    





# new_data = dataset.drop(existing_source_ids)
# incidents = map_df(new_data, create_orm)
    
    #COLUMNS =
    # Index(['uid', 'name', 'age', 'gender', 'raceethnicity', 'month', 'day', 'year',
    #    'streetaddress', 'city', 'state', 'classification',
    #    'lawenforcementagency', 'armed'],
    #   dtype='object')
    







    
