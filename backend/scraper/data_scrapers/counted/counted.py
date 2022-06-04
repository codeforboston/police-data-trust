import pandas as pd
import requests
import zipfile
import os
import glob
from collections import namedtuple

from scraper_utils import *
from .client import *
#from ....database import Incident

#extracts zipfile from Counted_Client function into cwd
def extract_zip():
    os.chdir('/Users/brianrennie/Documents/GitHub/police-data-trust/backend/scraper/data_scrapers/counted/scraper_data')
    curDir = os.getcwd()
    r = Counted_Client.run(self)
    open('thecounted-data.zip', 'wb').write(r.content)
    zf = zipfile.ZipFile(curDir + '/thecounted-data.zip')
    zf.extractall(curDir)
breakpoint()
#filters out any other filetype except .csv
def filter_csv():
    os.chdir('/Users/brianrennie/Documents/GitHub/police-data-trust/backend/scraper/data_scrapers/counted/scraper_data')
    curDir = os.getcwd()
    files = glob.glob(curDir + "/*.csv")
    return files

#creates dataframe and appends any other csv files
def append_dataframe():
    content = []
    filtered_files = filter_csv()
    for filename in filtered_files:
        df = pd.read_csv(filename, dtype={"uid": str}, index_col=None)
        content.append(df)
        counted_data = pd.concat(content)
    return counted_data

    
#convert colummns name to map to schema
def col_conv():
    df = append_dataframe()
    dataset = map_cols(df, {
        "uid": "source_id",
        "name": "victim_name",
        "gender": "victim_gender",
        "raceethnicity": "victim_race",
        "age": "victim_age",
        "URL of image of victim": "victim_image_url",
        "Cause of death": "manner_of_injury",
        "Date of Incident (month/day/year)": "incident_date",
        "streetaddress": "address",
        "city": "city",
        "state": "state",
     
    },).set_index("source_id", drop=False)
    return dataset
    print(dataset)
    #COLUMNS =
    # Index(['uid', 'name', 'age', 'gender', 'raceethnicity', 'month', 'day', 'year',
    #    'streetaddress', 'city', 'state', 'classification',
    #    'lawenforcementagency', 'armed'],
    #   dtype='object')
    







    
