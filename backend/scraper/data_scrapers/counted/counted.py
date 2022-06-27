from email import utils
import pandas as pd
import requests
import zipfile
import os
import glob
from collections import namedtuple
import sys
sys.path.append('/Users/brianrennie/Documents/GitHub/police-data-trust') 

from scraper_utils.utils import map_cols, map_df, create_bulk, create_orm
from counted.client import *

#extracts zipfile from Counted_Client function into cwd
def extract_zip():
    os.chdir('/Users/brianrennie/Documents/GitHub/police-data-trust/backend/scraper/data_scrapers/counted/scraper_data')
    curDir = os.getcwd()
    dataset = Counted_Client()
    r = dataset.run()
    open('thecounted-data.zip', 'wb').write(r.content)
    zf = zipfile.ZipFile(curDir + '/thecounted-data.zip')
    zf.extractall(curDir)

#filters out any other filetype except .csv
def filter_csv():
    os.chdir('/Users/brianrennie/Documents/GitHub/police-data-trust/backend/scraper/data_scrapers/counted/scraper_data')
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

if __name__ == '__main__':
    extract_zip()
    dataset = col_conv()
    incidents = create_incidents(dataset)
    append_to_index(incidents)
    





# new_data = dataset.drop(existing_source_ids)
# incidents = map_df(new_data, create_orm)
    
    #COLUMNS =
    # Index(['uid', 'name', 'age', 'gender', 'raceethnicity', 'month', 'day', 'year',
    #    'streetaddress', 'city', 'state', 'classification',
    #    'lawenforcementagency', 'armed'],
    #   dtype='object')
    







    
