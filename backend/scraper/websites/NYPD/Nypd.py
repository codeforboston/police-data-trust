import logging
import random
from backend.scraper.mixins.Scraper import ScraperMixin
from backend.scraper.mixins.Parser import ParserMixin
from backend.scraper.websites.NYPD.NYPDParser import NYPDParser


class Nypd(ScraperMixin, ParserMixin):
    OFFICER_CSV_PATH = "https://www.nyc.gov/assets/ccrb/csv/mos-history/DTI_MOS_History_w_MOSDisposition_MOSTable.CSV"  # noqa: E501
    INCIDENTS_CSV_PATH = "https://www.nyc.gov/assets/ccrb/csv/mos-history/DTI_MOS_History_w_MOSDisposition.CSV"  # noqa: E501
    RATE_LIMIT = 3

    def __init__(
        self,
    ):
        self.logger = logging.getLogger(__name__)
        super().__init__()
        self.rate_limit = self.RATE_LIMIT

    def _find_officers(self) -> list[str]:
        """Find all officers in a precinct"""
        resp = self.fetch(self.OFFICER_CSV_PATH)
        if not resp:
            self.logger.error(
                f"Could not fetch officers from {self.OFFICER_CSV_PATH}"
            )
            return []
        return resp.split("\n")[1:]

    def _find_incidents(self) -> list[str]:
        resp = self.fetch(self.INCIDENTS_CSV_PATH)
        if not resp:
            self.logger.error(
                f"Could not fetch incidents from {self.INCIDENTS_CSV_PATH}"
            )
            return []
        return resp.split("\n")[1:]

    def extract_data(self, debug: int = 0):
        """
        Extract the officer profiles from NYPD
        :param debug: The number of officers to extract (0 for all)
        :return: A tuple of officers and incidents
        """
        self.logger.info("Extracting data from NYPD")

        officers = self._find_officers()
        if debug:
            officers = random.sample(officers, debug)
        self.logger.info(f"Found {len(officers)} officers")

        incidents = self._find_incidents()
        if debug:
            incidents = random.sample(incidents, debug)
        self.logger.info(f"Found {len(incidents)} incidents")

        parser = NYPDParser()

        return parser.parse_officers(officers), parser.parse_incidents(
            incidents
        )
