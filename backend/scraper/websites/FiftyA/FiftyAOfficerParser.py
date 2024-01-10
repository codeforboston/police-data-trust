import re
import logging
from datetime import datetime
from bs4 import BeautifulSoup
from typing import Union, Optional
from dataclasses import dataclass

from backend.database import Officer, StateID
from backend.scraper.mixins.Parser import ParserMixin


@dataclass
class ParseOfficerReturn:
    officer: Officer
    complaints: list[str]
    work_history: list[str]


class FiftyAOfficerParser(ParserMixin):
    COMPLAINT_PATTERN = re.compile(r"^\/complaint\/\w+$")
    PRECINT_PATTERN = re.compile(r"^\/command\/\w+$")

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def _get_tax_id(self, soup: BeautifulSoup):
        return self._find_and_extract(
            soup, "span", "taxid", "No tax id found for officer", "Tax #"
        )

    def _get_complaints(self, soup: BeautifulSoup):
        complaint_links = soup.find_all("a", href=self.COMPLAINT_PATTERN)
        return [complaint.get("href") for complaint in complaint_links]

    def _get_work_history(self, soup: BeautifulSoup) -> list[str]:
        soup = soup.find("div", class_="commandhistory")  # type: ignore
        if not soup:
            self.logger.warning("Could not find work history div")
            return []
        work_history: list[str] = []
        work_history_links = soup.find_all("a", href=self.PRECINT_PATTERN)
        work_history += [work.text for work in work_history_links]
        return work_history

    def _calculate_date_of_birth(self, age: str) -> Union[str, None]:
        """Calculate date of birth from age"""
        if not age:
            return ""
        current_year = datetime.now().year
        return f"{current_year - int(age)}-01-01"

    def parse_officer(
        self, soup: BeautifulSoup
    ) -> Optional[ParseOfficerReturn]:
        if not soup:
            self.logger.error("Could not find identity div")
            return None

        officer: Officer = Officer()

        complaints = self._get_complaints(soup)

        tax_id = self._get_tax_id(soup)
        if not tax_id:
            self.logger.error("Officer does not have a tax id")
            return None
        stateId = StateID()
        stateId.id_name = "Tax ID Number"
        stateId.state = "NY"
        stateId.value = tax_id
        officer.stateId = stateId  # type: ignore

        title = self._find_and_extract(
            soup, "h1", "title name", "No title found for officer"
        )
        if title:
            first_name, last_name = (
                title.split(" ")
                if len(title.split(" ")) < 3
                else (title.split(" ")[0], title.split(" ")[2])
            )
            officer.first_name = first_name
            officer.last_name = last_name
        else:
            self.logger.error("No title found for officer")
            return None

        description = soup.find("span", class_="desc")  # type: ignore
        if description:
            description = description.text
            officer_descriptions = description.replace(",", "").split(" ")
            if len(officer_descriptions) == 3:
                (
                    officer.race,
                    officer.gender,
                    age,
                ) = officer_descriptions
                dob = self._calculate_date_of_birth(age)
                if dob:
                    officer.date_of_birth = dob
            else:
                self.logger.warning(
                    f"Could not parse officer description: {description}"
                )

        # TODO: Add rank and badge
        # rank = self._find_and_extract(
        #     soup, "span", "rank", "No rank found for officer", "Rank: "
        # )

        # badge = self._find_and_extract(
        #     soup, "span", "badge", "No badge found for officer", "Badge #: "
        # )

        work_history = self._get_work_history(soup)
        if work_history:
            self.logger.info(f"Found {len(work_history)} work history entries")
        return ParseOfficerReturn(
            officer=officer,
            complaints=complaints,
            work_history=work_history,
        )
