from ..database import Incident
from ..config import Config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .worker import app
import requests


config = Config()

# DB connection
engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


def get_or_create(session, model, **kwargs):
    # Update to allow for checking original incident ID
    try:
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            # if instance exsits
            # TODO: check if instance needs updating
            return instance
        else:
            instance = model(**kwargs)
            session.add(instance)
            session.commit()
            return instance
    except Exception as err:
        print(err)


@app.task(bind=True, name="refresh")
def refresh(self, urls):
    for url in urls:
        fetch_data(url)


@app.task(bind=True, name="fetch_data")
def fetch_data(self, url):
    session = Session()
    res = requests.get(url)
    try:
        if res.data:
            for data in res.data:
                get_or_create(session, Incident, data)
    except Exception as err:
        print(err)
