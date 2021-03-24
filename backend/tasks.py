from celery import Celery
# from celery.schedules import crontab
from celery.utils.log import get_task_logger
from incidents import Incidents
from config import Config
import requests
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = get_task_logger(__name__)

config = Config()

# DB connection
engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


app = Celery('tasks', backend='redis://redis:6379/0',
             broker='redis://redis:6379/0')


def get_or_create(session, model, **kwargs):
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


@app.task
def import_data(url):
    session = Session()
    res = requests.get(url)

    if res.content:
        for data in res.data:
            get_or_create(session, Incidents, data)

    return "Data added"
