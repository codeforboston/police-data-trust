import re
import logging
from bs4 import BeautifulSoup, Tag
from datetime import datetime
from typing import Optional
from backend.scraper.mixins.Parser import ParserMixin
from backend.database import (
    Incident,
    Victim,
    UseOfForce,
    SourceDetails,
    RecordType,
    Perpetrator,
)


class FiftyAIncidentParser(ParserMixin):
    LOCATION_REGEX = r"Location:\s*(.+)"
    PRECINCT_REGEX = r"In NYPD\s+(\S+)\s*Precinct\s*(.+)"
    TIME_FORMAT = "%m-%d-%Y %H:%M:%S"
    INCIDENT_REGEX = r"Incident: "
    REASON_FOR_CONTACT = "Reason for contact: "
    OUTCOME_REGEX = r"Outcome:.*\barrest\b"
    LINK_PATTERN = re.compile(r"^https://.*$")

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def _get_stop_type(self, details: list[str]) -> Optional[str]:
        reason = next(
            (
                item
                for item in details
                if re.search(re.escape("Reason for contact:"), item)
            ),
            None,
        )
        if reason:
            return reason.replace("Reason for contact:", "").strip()
        return None

    def _get_location(self, details_text: str) -> Optional[str]:
        location_match = re.search(self.LOCATION_REGEX, details_text)
        return location_match.group(1).strip() if location_match else None

    def _get_precinct(
        self, details_text: str
    ) -> tuple[Optional[str], Optional[str]]:
        precinct_match = re.search(
            self.PRECINCT_REGEX, details_text, re.IGNORECASE
        )
        precinct_number = (
            precinct_match.group(1).strip() if precinct_match else None
        )
        precinct_name = (
            precinct_match.group(2).strip() if precinct_match else None
        )
        return precinct_number, precinct_name

    def _parse_victim(self, soup: BeautifulSoup) -> list[Victim]:
        """
        Parse the victim's information from the soup object
        """
        complainant = soup.find("td", class_="complainant")
        if not complainant:
            return []

        age_tag = complainant.find("span", class_="age")  # type: ignore

        if age_tag and isinstance(age_tag, Tag):
            age = age_tag.get_text(strip=True)
            age_tag.decompose()  # remove the age tag from the complainant
        else:
            age = None
        age = age.split("-")[0] if age and "-" in age else age

        complainant_text = complainant.get_text(strip=True)
        if not complainant_text:
            return []
        complainant_text = (
            complainant_text.replace(age, "").replace(",", "").strip()
            if age
            else complainant_text.strip()
        )
        complainant_text = complainant_text.replace("\xa0", " ")
        gender_ethnicity = complainant_text.split(" ")
        if len(gender_ethnicity) == 2:
            ethnicity, gender = gender_ethnicity
        else:
            ethnicity = None
            gender = gender_ethnicity[0] if gender_ethnicity else None
        return [
            Victim(**{"ethnicity": ethnicity, "gender": gender, "age": age})
        ]

    def _get_force(self, soup: BeautifulSoup) -> Optional[list[UseOfForce]]:
        return [
            UseOfForce(**{"item": force})
            for force in list(
                {
                    allegation.text.strip().replace("Force: ", "")
                    for allegation in soup.find_all("td", class_="allegation")
                    if "Force: " in allegation.text.strip()
                }
            )
        ]

    def _get_officers(self, soup: BeautifulSoup) -> list[Perpetrator]:
        officer_involved = set(soup.find_all("a", class_="name"))
        badge_number_pattern = re.compile(r"#(\w+)$")
        perps: list[Perpetrator] = []
        for officer in officer_involved:
            description = officer.get_text(strip=True)
            badge = re.search(badge_number_pattern, description)
            if badge:
                badge = badge.group(1)
            title = officer.get("title", "").split(" ")[0]
            mapping = {"Police": "OFFICER", "Sergeant": "SERGEANT"}
            title = mapping.get(title, "OFFICER")
            perps.append(
                Perpetrator(
                    **{
                        "badge": badge,
                        "first_name": description.split(" ")[0],
                        "last_name": description.split(" ")[-1],
                        "rank": title,
                    }
                )
            )
        return perps

    def _get_witnesses(self, details: list[str]) -> Optional[list[str]]:
        witnesses: list[str] = []
        add_flag = False
        for detail in details:
            if add_flag:
                witnesses.append(detail)
            if detail == "Witness Officers:":
                add_flag = True
        return witnesses

    def complaint_number(self, complaint_link: str) -> str:
        """
        Get the complaint number from the complaint link
        """
        return complaint_link.split("/")[-1]

    def parse_complaint(
        self, complaint_html: str, complaint_link: str
    ) -> Optional[Incident]:
        """
        Parse a complaint
        """
        soup = BeautifulSoup(complaint_html, "html.parser")

        details_text = self._find_and_extract(
            soup, "div", "details", "No details found for complaint"
        )
        if not details_text:
            return None
        details = [
            detail.strip()
            for detail in details_text.split("\n")
            if detail.strip()
        ]

        links = soup.find_all("a", href=self.LINK_PATTERN)

        incident_location = self._get_location(details_text)
        precinct_number, precinct_name = self._get_precinct(details_text)

        incident = Incident()
        incident.date_record_created = datetime.now().strftime(self.TIME_FORMAT)
        incident.time_of_incident = datetime.strptime(
            details[0].replace("Received: ", "").replace("Incident: ", ""),
            "%B %d, %Y",
        ).strftime(self.TIME_FORMAT)
        incident.description = f"Incident scraped from: {complaint_link}"
        incident.location = (
            f"{incident_location} In NYPD {precinct_number} Precinct {precinct_name}"  # noqa: E501
            if incident_location and precinct_number and precinct_name
            else None
        )
        incident.longitude = 40.7128
        incident.latitude = 74.0060
        incident.stop_type = self._get_stop_type(details)
        incident.call_type = self._get_stop_type(details)
        incident.has_attachments = bool(links)
        incident.from_report = True
        incident.was_victim_arrested = bool(
            re.compile(self.OUTCOME_REGEX, re.IGNORECASE).search(details_text)
        )
        incident.arrest_id = None
        incident.criminal_case_brought = None
        incident.case_id = None

        # TODO: Add backrefs to database
        victim = self._parse_victim(soup)
        force = self._get_force(soup)

        source = SourceDetails(
            **{
                "record_type": RecordType.GOVERNMENT_RECORD,
                "reporting_organization": "FiftyA",
                "reporting_organization_url": complaint_link,
                "reporting_organization_email": "f12@50-a.org",
            }
        )
        incident.source_details = source  # type: ignore
        incident.victims = victim  # type: ignore
        incident.use_of_force = force  # type: ignore
        incident.case_id = int(self.complaint_number(complaint_link))
        incident.perpetrators = self._get_officers(soup)  # type: ignore # noqa: E501
        return incident
