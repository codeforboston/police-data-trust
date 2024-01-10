import re
import time
import random
from bs4 import BeautifulSoup
from backend.scraper.mixins.Scraper import ScraperMixin
from backend.scraper.mixins.Parser import ParserMixin
from backend.scraper.websites.FiftyA.FiftyAOfficerParser import FiftyAOfficerParser
from backend.scraper.websites.FiftyA.FiftyAIncidentParser import FiftyAIncidentParser
from backend.database import Officer, Incident


class FiftyA(ScraperMixin, ParserMixin):
    SEED = "https://www.50-a.org"
    RATE_LIMIT = 3
    COMPLAINT_PATTERN = re.compile(r"^\/complaint\/\w+$")
    OFFICER_PATTERN = re.compile(r"^\/officer\/\w+$")
    PRECINT_PATTERN = re.compile(r"^\/command\/\w+$")

    def __init__(self):
        super().__init__()
        self.rate_limit = self.RATE_LIMIT

    def _find_officers(self, precinct: str) -> list[str]:
        """Find all officers in a precinct"""
        precinct_url = f"{self.SEED}{precinct}"
        officers = self.find_urls(precinct_url, self.OFFICER_PATTERN)
        self.logger.info(f"Found {len(officers)} officers in precinct {precinct}")
        return officers

    def extract_data(self, debug: bool = False) -> tuple[list[Officer], list[Incident]]:
        """Extract the officer profiles from 50a"""
        precincts: list[str] = self.find_urls(
            f"{self.SEED}/commands", self.PRECINT_PATTERN
        )
        self.logger.info(f"Found {len(precincts)} precincts")
        officers: list[str] = []

        if debug:
            precincts = random.sample(precincts, 5)

        for index, precinct in enumerate(precincts):
            if index % 10 == 0 and index != 0:
                self.logger.info(
                    f"Scrapped {index} precincts and have found {len(officers)} officers"
                )
            time.sleep(self.RATE_LIMIT)
            officers += self._find_officers(precinct)

        self.logger.info(f"Found {len(officers)} officers")

        officer_profiles: list[Officer] = []
        complaints: list[str] = []
        if debug:
            officers = random.sample(officers, min(5, len(officers)))
        officer_parser = FiftyAOfficerParser()
        for index, officer in enumerate(officers):
            if index % 10 == 0 and index != 0:
                self.logger.info(
                    f"Scrapped {index} officers and have found {len(officer_profiles)} officer profiles"
                )
            response = self.fetch(f"{self.SEED}{officer}")
            if not response:
                continue
            officer_data = officer_parser.parse_officer(
                BeautifulSoup(response, "html.parser")
            )
            if not officer_data:
                continue

            complaints += officer_data.complaints
            if officer_data.officer:
                officer_profiles.append(officer_data.officer)

        self.logger.info(f"Found {len(complaints)} complaints")

        if debug:
            complaints = random.sample(complaints, min(5, len(complaints)))

        incidents: list[Incident] = []
        incident_parser = FiftyAIncidentParser()
        for index, complaint in enumerate(complaints):
            if index % 10 == 0 and index != 0:
                self.logger.info(f"Scrapped {index} complaints")
            response = self.fetch(f"{self.SEED}{complaint}")
            if not response:
                continue

            incident = incident_parser.parse_complaint(response, complaint)
            if incident:
                incidents.append(incident)
        return officer_profiles, incidents
