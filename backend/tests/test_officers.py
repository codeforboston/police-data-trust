from __future__ import annotations
from unittest import TestCase

import math
from backend.database import (
    Officer,
)

mock_officers = {
    "john": {
        "first_name": "John",
        "last_name": "Doe",
        "race": "White",
        "ethnicity": "Non-Hispanic",
        "gender": "M",
    },
    "hazel": {
        "first_name": "Hazel",
        "last_name": "Nutt",
        "race": "White",
        "ethnicity": "Non-Hispanic",
        "gender": "F",
    },
    "frank": {
        "first_name": "Frank",
        "last_name": "Furter",
        "race": "Black",
        "ethnicity": "African American",
        "gender": "M",
    },
}

mock_agencies = {
    "cpd": {
        "name": "Chicago Police Department",
        "website_url": "https://www.chicagopolice.org/",
        "hq_address": "3510 S Michigan Ave",
        "hq_city": "Chicago",
        "hq_zip": "60653",
        "jurisdiction": "MUNICIPAL",
    },
    "nypd": {
        "name": "New York Police Department",
        "website_url": "https://www1.nyc.gov/site/nypd/index.page",
        "hq_address": "1 Police Plaza",
        "hq_city": "New York",
        "hq_zip": "10038",
        "jurisdiction": "MUNICIPAL",
    },
}

mock_employment = {
    "john": {
        "agency": "Chicago Police Department",
        "earliest_employment": "2015-03-14 00:00:00",
        "badge_number": "1234",
        "currently_employed": True,
    },
    "hazel": {
        "agency": "Chicago Police Department",
        "earliest_employment": "2018-08-12 00:00:00",
        "badge_number": "5678",
        "currently_employed": True,
    },
    "frank": {
        "agency": "New York Police Department",
        "earliest_employment": "2019-05-03 00:00:00",
        "badge_number": "1234",
        "currently_employed": True,
    },
}

mock_incidents = {
    "domestic": {
        "time_of_incident": "2021-03-14 01:05:09",
        "description": "Domestic disturbance",
        "perpetrators": [
            {"first_name": "Decent", "last_name": "Cop"},
        ],
        "use_of_force": [{"item": "Injurious restraint"}],
        "source": "Citizens Police Data Project",
        "location": "123 Right St Chicago, IL",
    },
    "traffic": {
        "time_of_incident": "2021-10-01 00:00:00",
        "description": "Traffic stop",
        "perpetrators": [
            {"first_name": "Bad", "last_name": "Cop"},
        ],
        "use_of_force": [{"item": "verbalization"}],
        "source": "Mapping Police Violence",
        "location": "Park St and Boylston Boston",
    },
    "firearm": {
        "time_of_incident": "2021-10-05 00:00:00",
        "description": "Robbery",
        "perpetrators": [
            {"first_name": "Bad", "last_name": "Cop"},
        ],
        "use_of_force": [{"item": "indirect firearm"}],
        "source": "Citizens Police Data Project",
        "location": "CHICAGO ILLINOIS",
    },
}

mock_partners = {"cpdp": {"name": "Citizens Police Data Project"}}

mock_accusations = {
    "domestic": {
        "officer": "light",
        "date_created": "2023-03-14 01:05:09",
        "basis": "Name Match",
    },
    "traffic": {
        "officer": "severe",
        "date_created": "2023-10-01 00:00:00",
        "basis": "Name Match",
    },
    "firearm": {
        "officer": "severe",
        "date_created": "2023-10-05 00:00:00",
        "basis": "Name Match",
    },
}


class TestOfficers(TestCase):
    def test_create_officer(
        self, db_session, client, contributor_access_token, example_agency
    ):

        # Test that we can create an officer with an agency association
        request = {
            "first_name": "Max",
            "last_name": "Payne",
            "race": "White",
            "ethnicity": "Non-Hispanic",
            "gender": "M",
            "agency_association": [
                {
                    "agency_id": example_agency.id,
                    "earliest_employment": "2015-03-14 00:00:00",
                    "badge_number": "8349",
                    "currently_employed": True,
                }
            ],
        }
        res = client.post(
            "/api/v1/officers/",
            json=request,
            headers={"Authorization": f"Bearer {contributor_access_token}"},
        )
        self.assertEqual(res.status_code, 200)
        response = res.json

        officer_obj = (
            db_session.query(Officer)
            .filter(Officer.id == response["id"])
            .first()
        )
        self.assertEqual(officer_obj.first_name, request["first_name"])
        self.assertEqual(officer_obj.last_name, request["last_name"])
        self.assertEqual(officer_obj.race, request["race"])
        self.assertEqual(officer_obj.ethnicity, request["ethnicity"])
        self.assertEqual(
            len(officer_obj.agency_association),
            len(request["agency_association"]),
        )
        self.assertEqual(
            officer_obj.agency_association[0].badge_number,
            request["agency_association"][0]["badge_number"],
        )
        self.assertEqual(
            officer_obj.agency_association[0].agency_id, example_agency.id
        )

        # Test that we can create an officer without an agency association
        request = {
            "first_name": "Max",
            "last_name": "Payne",
            "race": "White",
            "ethnicity": "Non-Hispanic",
            "gender": "M",
        }
        res = client.post(
            "/api/v1/officers/",
            json=request,
            headers={"Authorization": f"Bearer {contributor_access_token}"},
        )
        self.assertEqual(res.status_code, 200)
        response = res.json

        officer_obj = (
            db_session.query(Officer)
            .filter(Officer.id == response["id"])
            .first()
        )
        self.assertEqual(officer_obj.first_name, request["first_name"])
        self.assertEqual(officer_obj.last_name, request["last_name"])
        self.assertEqual(officer_obj.race, request["race"])
        self.assertEqual(officer_obj.ethnicity, request["ethnicity"])

    def test_get_officer(self, client, example_officer, access_token):
        # Test that we can get it
        res = client.get(f"/api/v1/officers/{example_officer.id}")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json["first_name"], example_officer.first_name)
        self.assertEqual(res.json["last_name"], example_officer.last_name)

    """
    def test_search_officers(self, client, example_officers, access_token):
        for query, expected_officer_names in {
            {}: ["severe", "light", "none"],
            {"location": "New York"}: ["none"],
            {"badgeNumber": "1234"}: ["severe", "none"],
            {"name": "Decent"}: ["light"],
        }.items():
            res = client.post(
                "/api/v1/officers/search",
                json=query,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            self.assertEqual(res.status_code, 200)

            # Match the results to the known dataset and assert that
            # all the expected results are present
            actual_officers = res.json["results"]

            def officer_name(officer):
                return next(
                    (
                        k
                        for k, v in example_officers.items()
                        if v["id"] == officer["id"]
                    ),
                    None,
                )

            actual_incident_names = list(
                filter(None, map(officer_name, actual_officers))
            )
            self.assertSetEqual(
                set(actual_incident_names), set(expected_officer_names)
            )

            self.assertEqual(res.json["page"], 1)
            self.assertEqual(res.json["totalPages"], 1)
            self.assertEqual(
                res.json["totalResults"], len(expected_officer_names)
            )
    """

    def test_get_officers(self, client, db_session, access_token):
        # Create Officers in the database
        for name, mock in mock_officers.items():
            db_session.add(Officer(**mock))
        db_session.commit()

        res = client.get(
            "/api/v1/officers/",
            headers={"Authorization ": f"Bearer {access_token}"},
        )

        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res.json["results"][0]["first_name"])
        self.assertIsNotNone(res.json["results"][0]["last_name"])
        self.assertEqual(res.json["page"], 1)
        self.assertEqual(res.json["totalPages"], 1)
        self.assertEqual(res.json["totalResults"], len(mock_officers))

        test_officer = res.json["results"][0]
        single_res = client.get(
            f"/api/v1/officers/{test_officer['id']}",
            headers={"Authorization ": f"Bearer {access_token}"},
        )
        self.assertEqual(test_officer, single_res.json)

    def test_officer_pagination(self, client, db_session, access_token):
        # Create Officers in the database
        created_officers = []
        for name, mock in mock_officers.items():
            db_session.add(Officer(**mock))
            created_officers.append(Officer(**mock))
        db_session.commit()

        per_page = 1
        expected_total_pages = math.ceil(len(mock_officers) // per_page)

        for page in range(1, expected_total_pages + 1):
            res = client.get(
                "/api/v1/officers/",
                query_string={"per_page": per_page, "page": page},
                headers={"Authorization": f"Bearer {access_token}"},
            )

            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json["page"], page)
            self.assertEqual(res.json["totalPages"], expected_total_pages)
            self.assertEqual(res.json["totalResults"], len(mock_officers))
            self.assertEqual(len(res.json["results"]), per_page)

        res = client.get(
            "/api/v1/officers/",
            query_string={
                "perPage": per_page,
                "page": expected_total_pages + 1,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(res.status_code, 404)

    """
    def test_get_accusations(self, client: Any, access_token: str):
        res = client.get(
            "/api/v1/officers/",
            headers={"Authorization ": f"Bearer {access_token}"},
        )

        self.assertEqual(res.status_code, 200)
        self.assertListEqual(res.json["results"], [])
        self.assertEqual(res.json["page"], 1)
        self.assertEqual(res.json["totalPages"], 0)
        self.assertEqual(res.json["totalResults"], 0)

    def test_get_accusations_pagination(
        self,
        client: Any,
        access_token: str,
        example_incidents_private_public: list[Incident],
    ):
        \"""
        Test that pagination works for public incidents.
        \"""
        res = client.get(
            "/api/v1/officers/?per_page=1",
            headers={"Authorization ": f"Bearer {access_token}"},
        )

        public_incidents_count = len(
            [
                i
                for i in example_incidents_private_public
                if i.privacy_filter == PrivacyStatus.PUBLIC
            ]
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json["results"]), 1)
        self.assertEqual(res.json["page"], 1)
        self.assertEqual(res.json["totalPages"], public_incidents_count)
        self.assertEqual(res.json["totalResults"], public_incidents_count)

        res = client.get(
            "/api/v1/officers/?per_page=1&page=2",
            headers={"Authorization ": f"Bearer {access_token}"},
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json["results"]), 0)
        self.assertEqual(res.json["page"], 2)
        self.assertEqual(res.json["totalPages"], public_incidents_count)
        self.assertEqual(res.json["totalResults"], public_incidents_count)

    def test_get_employers(
        self,
        client: Any,
        access_token: str,
        example_incidents_private_public: list[Incident],
    ):
        \"""
        Test that a regular user can see public incidents.
        \"""

        res = client.get(
            "/api/v1/officers/",
            headers={"Authorization ": f"Bearer {access_token}"},
        )

        public_incidents_count = len(
            [
                i
                for i in example_incidents_private_public
                if i.privacy_filter == PrivacyStatus.PUBLIC
            ]
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json["results"]), public_incidents_count)
        self.assertEqual(res.json["page"], 1)
        self.assertEqual(res.json["totalPages"], 1)
        self.assertEqual(res.json["totalResults"], public_incidents_count)

    def test_get_employers_pagination(
        self,
        client: Any,
        access_token: str,
        example_incidents_private_public: list[Incident],
    ):
        \"""
        Test that pagination works for public incidents.
        \"""
        res = client.get(
            "/api/v1/officers/?per_page=1",
            headers={"Authorization ": f"Bearer {access_token}"},
        )

        public_incidents_count = len(
            [
                i
                for i in example_incidents_private_public
                if i.privacy_filter == PrivacyStatus.PUBLIC
            ]
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json["results"]), 1)
        self.assertEqual(res.json["page"], 1)
        self.assertEqual(res.json["totalPages"], public_incidents_count)
        self.assertEqual(res.json["totalResults"], public_incidents_count)

        res = client.get(
            "/api/v1/officers/?per_page=1&page=2",
            headers={"Authorization ": f"Bearer {access_token}"},
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json["results"]), 0)
        self.assertEqual(res.json["page"], 2)
        self.assertEqual(res.json["totalPages"], public_incidents_count)
        self.assertEqual(res.json["totalResults"], public_incidents_count)

    def test_delete_officer(
        self,
        client: Any,
        partner_publisher: User,
        example_partner: Partner,
        example_incidents_private_public: list[Incident],
    ):
        \"""
        Test that a partner member can delete an incident.
        \"""

        access_token = res = client.post(
            "api/v1/auth/login",
            json={
                "email": partner_publisher.email,
                "password": "my_password",
            },
        ).json["access_token"]

        # Make a request to delete the incident
        res = client.delete(
            f"/api/v1/officers/{example_incidents_private_public[0].id}"
            + f"?partner_id={example_partner.id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(res.status_code, 204)

        # Verify that the incident is deleted
        deleted_incident = Incident.query.get(
            example_incidents_private_public[0].id
        )
        self.assertIsNone(deleted_incident)

    def test_delete_officer_no_user_role(
        self,
        client: Any,
        access_token: str,
    ):
        \"""
        Test that a user without atlest CONTRIBUTOR role
        can't delete an incident.
        \"""
        # Make a request to delete the incident
        res = client.delete(
            "/api/v1/officers/1",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        self.assertEqual(res.status_code, 403)
    """
