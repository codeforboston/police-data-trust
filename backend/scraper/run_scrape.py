import logging
from backend.scraper.websites.FiftyA.FiftyA import FiftyA
from backend.scraper.websites.NYPD.Nypd import Nypd
from backend.scraper.mixins.ScrapeCache import ScrapeCacheContainer, ScrapeCache
from backend.database import Officer, Incident, StateID, db
from typing import Union
from sqlalchemy.orm import Session, scoped_session


def officer_exists(
    session: scoped_session[Session], state_id_value: str
) -> bool:
    return (
        session.query(Officer)
        .join(StateID)
        .filter(StateID.value == state_id_value)
        .first()
        is not None
    )


def incident_exists(session: Session, case_id: str) -> bool:
    return (
        session.query(Incident).filter(Incident.case_id == case_id).first()
        is not None
    )


def add_to_database(
    model: Union[Officer, Incident], cache: ScrapeCache, uid: str, table: str
):
    logger = logging.Logger("scrape")
    if cache.get_json(uid, table):
        logger.info(f"{table} {uid} already in cache")
        return

    # add the model to the database
    # Check if the model already exists in the database
    model_exists: bool
    if table == "officer":
        model_exists = officer_exists(
            db.session,  # type: ignore
            model.stateId.value,  # type: ignore
        )
    elif table == "incident":
        model_exists = incident_exists(
            db.session,  # type: ignore
            model.case_id,  # type: ignore
        )
    else:
        raise ValueError(f"Invalid table {table}")
    if model_exists:  # type: ignore
        logger.info(f"{table} {uid} already in database")
        return

    model.create()

    # add the model to the cache
    model_dict = model.__getstate__()
    try:
        cache.set_json(uid, model_dict, table)
    except Exception as e:
        logger.error(f"Failed to add {table} {uid} to cache: {e}")


def scrape(debug: bool = False):
    logger = logging.Logger("scrape")
    logger.info("Starting scrape")

    # Read the data from FiftyA
    fiftya = FiftyA()
    fiftya_officer, fiftya_incidents = fiftya.extract_data(debug=debug)

    logger.info(
        f"Found {len(fiftya_officer)} officers and {len(fiftya_incidents)}\
        incidents from FiftyA"
    )

    # read the data from NYPD and merge it with FiftyA
    nypd = Nypd()
    nypd_officer, nypd_incidents = nypd.extract_data(debug=debug)

    logger.info(
        f"Found {len(nypd_officer)} officers and {len(nypd_incidents)}incidents from NYPD"  # noqa: E501
    )

    officers = fiftya_officer + nypd_officer
    incidents = fiftya_incidents + nypd_incidents

    # Connect to the cache and a producer
    cache_container = ScrapeCacheContainer("REDIS")
    cache = cache_container.get_cache()

    for officer in officers:
        uid = f"{officer.stateId.state}/{ officer.stateId.value}"
        add_to_database(officer, cache, uid, "officer")

    for incident in incidents:
        uid = f"{incident.source_details.reporting_organization}/{incident.case_id}"  # noqa: E501
        add_to_database(incident, cache, uid, "incident")
