import re
import time
import random
from bs4 import BeautifulSoup
from backend.scraper.mixins.Scraper import ScraperMixin
from backend.scraper.mixins.Parser import ParserMixin
from backend.scraper.websites.FiftyA.FiftyAOfficerParser import (
    FiftyAOfficerParser,
)
from backend.scraper.websites.FiftyA.FiftyAIncidentParser import (
    FiftyAIncidentParser,
)
from backend.database import Officer, Incident


class FiftyA(ScraperMixin, ParserMixin):
    SEED = "https://www.50-a.org"
    RATE_LIMIT = 3
    DEBUG_SAMPLE_SIZE = 5
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
        self.logger.info(
            f"Found {len(officers)} officers in precinct {precinct}"
        )
        return officers

    def sample_list(self, list: list[str], num: int) -> list[str]:
        return random.sample(list, min(num, len(list)))

    def _find_officers_in_precincts(self, debug: bool) -> list[str]:
        precincts: list[str] = self.find_urls(
            f"{self.SEED}/commands", self.PRECINT_PATTERN
        )
        self.logger.info(f"Found {len(precincts)} precincts")

        if debug:
            precincts = self.sample_list(
                precincts, min(self.DEBUG_SAMPLE_SIZE, len(precincts))
            )
        officers: list[str] = []
        for index, precinct in enumerate(precincts):
            if index % 10 == 0 and index != 0:
                self.logger.info(
                    f"Scrapped {index} precincts and have found {len(officers)} officers"  # noqa: E501
                )
            time.sleep(self.RATE_LIMIT)
            officers += self._find_officers(precinct)

        self.logger.info(f"Found {len(officers)} officers")
        return officers

    def _find_incidents(self, complaints: list[str]) -> list[Incident]:
        incidents: list[Incident] = []
        incident_parser = FiftyAIncidentParser()
        for index, complaint in enumerate(complaints):
            if index % 10 == 0 and index != 0:
                self.logger.info(f"Scrapped {index} complaints")
            response = self.fetch(f"{self.SEED}{complaint}")
            if not response:
                self.logger.error(f"Could not fetch {complaint}")
                continue

            incident = incident_parser.parse_complaint(response, complaint)
            if incident:
                incidents.append(incident)
        return incidents

    def _find_officer_profile_and_complaints(
        self, officers: list[str]
    ) -> tuple[list[Officer], list[str]]:
        officer_profiles: list[Officer] = []
        complaints: list[str] = []
        officer_parser = FiftyAOfficerParser()
        for index, officer in enumerate(officers):
            if index % 10 == 0 and index != 0:
                self.logger.info(
                    f"Scrapped {index} officers and have found {len(officer_profiles)} officer profiles"  # noqa: E501
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
        return officer_profiles, complaints

    def extract_data(
        self, debug: bool = False
    ) -> tuple[list[Officer], list[Incident]]:
        """Extract the officer profiles from 50a"""
        officers = self._find_officers_in_precincts(debug=debug)

        if debug:
            officers = random.sample(
                officers, min(self.DEBUG_SAMPLE_SIZE, len(officers))
            )
        (
            officer_profiles,
            complaints,
        ) = self._find_officer_profile_and_complaints(officers)

        if debug:
            complaints = random.sample(
                complaints, min(self.DEBUG_SAMPLE_SIZE, len(complaints))
            )
        incidents = self._find_incidents(complaints)
        return officer_profiles, incidents
