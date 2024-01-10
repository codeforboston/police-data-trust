import logging
from backend.scraper.websites.FiftyA.FiftyA import FiftyA
from backend.scraper.websites.NYPD.Nypd import Nypd
from backend.scraper.mixins.ScrapeCache import ScrapeCacheContainer


def scrape(debug: bool = False):
    logger = logging.Logger("scrape")
    logger.info("Starting scrape")

    # Read the data from FiftyA
    fiftya = FiftyA()
    fiftya_officer, fiftya_incidents = fiftya.extract_data(debug=debug)

    logger.info(
        f"Found {len(fiftya_officer)} officers and {len(fiftya_incidents)} incidents from FiftyA"
    )

    # read the data from NYPD and merge it with FiftyA
    nypd = Nypd()
    nypd_officer, nypd_incidents = nypd.extract_data(debug=debug)

    logger.info(
        f"Found {len(nypd_officer)} officers and {len(nypd_incidents)} incidents from NYPD"
    )

    officers = fiftya_officer + nypd_officer
    incidents = fiftya_incidents + nypd_incidents

    # Connect to the cache and a producer
    cache_container = ScrapeCacheContainer("REDIS")
    cache = cache_container.get_cache()

    for officer in officers:
        uid = f"{officer.stateId.state}/{ officer.stateId.value}"
        if cache.get_json(uid, "officer"):
            logger.info(f"Officer {uid} already in cache")
            continue

        # add the officer and stateId to the database
        officer.create()

        # add the officer to the cache
        officer_dict = officer.__getstate__()
        try:
            cache.set_json(uid, officer_dict, "officer")
        except Exception as e:
            logger.error(f"Failed to add officer {uid} to cache: {e}")

    for incident in incidents:
        uid = f"{incident.source_details.reporting_organization}/{incident.case_id}"
        if cache.get_json(uid, "incident"):
            logger.info(f"Incident {uid} already in cache")
            continue

        # add the incident to the database
        incident.create()

        # add the incident to the cache
        incident_dict = incident.__getstate__()
        try:
            cache.set_json(uid, incident_dict, "incident")
        except Exception as e:
            logger.error(f"Failed to add incident {uid} to cache: {e}")
