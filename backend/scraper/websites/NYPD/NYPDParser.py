from backend.database import Officer, Incident, StateID, SourceDetails, RecordType


class NYPDParser:
    def parse_officers(self, officers: list[str]) -> list[Officer]:
        """Parse the officers from the csv file
        TODO: https://nypdonline.org/link/2 -> get more info on officer
        """
        parsed_officers: list[Officer] = []
        for officer in officers:
            officer_csv = officer.split(",")
            officer = Officer()
            officer.first_name = officer_csv[3]
            officer.last_name = officer_csv[4]
            stateid = StateID()
            stateid.id_name = "Tax ID Number"
            stateid.state = "NY"
            stateid.value = officer_csv[5]
            officer.stateId = stateid  # type: ignore
            # officer.tax_id = officer_csv[5]
            parsed_officers.append(officer)
        return parsed_officers

    def parse_incidents(self, incidents: list[str]) -> list[Incident]:
        """Parse the incidents from the csv file"""

        parsed_incidents: list[Incident] = []

        for incident in incidents:
            incident_csv = incident.split(",")
            incident = Incident()
            incident.time_of_incident = incident_csv[13]  # Incident Date
            incident.description = incident_csv[15]  # Allegation
            incident.location = incident_csv[10]
            incident.longitude = 40.7128
            incident.latitude = 74.0060
            incident.stop_type = incident_csv[14]  # FADO Type
            incident.call_type = incident_csv[14]
            incident.has_attachments = False
            incident.from_report = True
            incident.was_victim_arrested = False
            incident.arrest_id = None
            incident.criminal_case_brought = None
            incident.case_id = incident_csv[12]
            source = SourceDetails(
                **{
                    "record_type": RecordType.GOVERNMENT_RECORD,
                    "reporting_organization": "NYPD",
                    "reporting_organization_url": "https://www.nyc.gov/site/ccrb/policy/MOS-records.page",
                }
            )
            incident.source_details = source  # type: ignore
            parsed_incidents.append(incident)
        return parsed_incidents
