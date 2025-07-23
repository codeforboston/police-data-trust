from __future__ import annotations
import pytest
import math
from datetime import date
from backend.database import (
    Complaint, Source, Officer
)

mock_complaint = {
    "record_id": "202202712",
    "source_details": {
        "record_type": "government",
        "reporting_agency": "New York City Civilian Complaint Review Board",
        "reporting_agency_url": "https://www.nyc.gov/site/ccrb/index.page",
        "reporting_agency_email": None
    },
    "category": None,
    "incident_date": "2022-04-15",
    "received_date": "2022-04-29",
    "closed_date": "2023-07-20",
    "location": {
        "location_type": "Subway station/train",
        "location_description": "Midtown North Precinct, Manhattan",
        "address": None,
        "city": "Manhattan",
        "state": "NY",
        "zip": None,
        "administrative_area": "Midtown North Precinct",
        "administrative_area_type": "precinct"
    },
    "reason_for_contact": "C/V intervened on behalf"
    " of/observed encounter w/3rd party",
    "outcome_of_contact": "Arrest - disorderly conduct",
    "civilian_witnesses": None,
    "attachments": [
        {
            "filetype": "application/pdf",
            "url": "https://www.documentcloud.org/documents/"
            "25189362-202202712_redactedclosingreportpdf",
            "title": "Complaint Closing Report"
        }
    ],
    "civilian_review_board_uid": None,
    "police_witnesses": None,
    "allegations": [
        {
            "record_id": None,
            "complainant": {
                "age": 37,
                "age_range": "35-39",
                "ethnicity": None,
                "gender": "Male"
            },
            "allegation": "Refusal to process civilian complaint",
            "type": "Abuse of Authority",
            "subtype": None,
            "recommended_finding": None,
            "recommended_outcome": None,
            "finding": "Substantiated",
            "outcome": "Command Discipline B"
        }
    ],
    "investigations": None,
    "penalties": [
        {
            "crb_plea": None,
            "crb_case_status": None,
            "crb_disposition": None,
            "agency_disposition": "Substantiated",
            "penalty": "Command Discipline B",
            "date_assessed": "2023-07-20"
        }
    ]
}


def test_create_complaint(
        db_session,
        client,
        contributor_access_token,
        example_source: Source,
        example_officer: Officer,
):
    """
    Test that we can create a complaint.
    """
    request = {
        "record_id": mock_complaint["record_id"],
        "source_details": mock_complaint["source_details"],
        "category": mock_complaint["category"],
        "incident_date": mock_complaint["incident_date"],
        "received_date": mock_complaint["received_date"],
        "closed_date": mock_complaint["closed_date"],
        "location": mock_complaint["location"],
        "reason_for_contact": mock_complaint["reason_for_contact"],
        "outcome_of_contact": mock_complaint["outcome_of_contact"],
        "source_uid": example_source.uid,
        "attachments": mock_complaint["attachments"],
        "allegations": mock_complaint["allegations"],
        "penalties": mock_complaint["penalties"],
    }
    request['allegations'][0]['accused_uid'] = example_officer.uid
    request['penalties'][0]['officer_uid'] = example_officer.uid
    res = client.post(
        "/api/v1/complaints/",
        json=request,
        headers={
            "Authorization": "Bearer {0}".format(contributor_access_token)
        },
    )
    assert res.status_code == 201
    response = res.json

    c = (
       Complaint.nodes.get(uid=response["uid"])
    )
    assert c.record_id == request["record_id"]
    assert c.category == request["category"]
    assert c.reason_for_contact == request["reason_for_contact"]
    assert c.outcome_of_contact == request["outcome_of_contact"]
    assert c.incident_date == date.fromisoformat(request["incident_date"])
    assert c.received_date == date.fromisoformat(request["received_date"])
    assert c.closed_date == date.fromisoformat(request["closed_date"])

    location = c.location.single()
    source_obj = c.source_org.single()
    source_rel = c.source_org.relationship(source_obj)
    attachment_obj = c.attachments.single()
    allegation_obj = c.allegations.single()
    complainant_obj = allegation_obj.complainant.single()
    penalty_obj = c.penalties.single()

    for prop, value in request["location"].items():
        assert getattr(location, prop) == value
    for prop, value in request["source_details"].items():
        assert getattr(source_rel, prop) == value
    for prop, value in request["attachments"][0].items():
        assert getattr(attachment_obj, prop) == value
    for prop, value in request["allegations"][0].items():
        if prop == "accused_uid":
            assert allegation_obj.accused.single().uid == value
        elif prop == "complainant":
            for sub_prop, sub_value in value.items():
                assert getattr(complainant_obj, sub_prop) == sub_value
        else:
            assert getattr(allegation_obj, prop) == value
    for prop, value in request["penalties"][0].items():
        if prop == "officer_uid":
            assert penalty_obj.officer.single().uid == value
        elif prop == "date_assessed":
            assert penalty_obj.date_assessed == date.fromisoformat(value)
        else:
            assert getattr(penalty_obj, prop) == value


def test_create_complaint_no_permission(
        client, access_token, example_complaint, example_source):

    request = {
        "record_id": mock_complaint["record_id"],
        "source_details": mock_complaint["source_details"],
        "category": mock_complaint["category"],
        "incident_date": mock_complaint["incident_date"],
        "received_date": mock_complaint["received_date"],
        "closed_date": mock_complaint["closed_date"],
        "location": mock_complaint["location"],
        "reason_for_contact": mock_complaint["reason_for_contact"],
        "outcome_of_contact": mock_complaint["outcome_of_contact"],
        "source_uid": example_source.uid,
        "attachments": mock_complaint["attachments"],
        "allegations": mock_complaint["allegations"],
        "penalties": mock_complaint["penalties"],
    }

    res = client.post(
        "/api/v1/complaints/",
        json=request,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 403


def test_get_complaint(client, db_session, example_complaint, access_token):
    """Test that we can retrieve a complaint by its UID.
    """
    res = client.get(f"/api/v1/complaints/{example_complaint.uid}")

    assert res.status_code == 200
    assert res.json["record_id"] == example_complaint.record_id
    assert res.json["category"] == example_complaint.category
    assert res.json[
        "reason_for_contact"] == example_complaint.reason_for_contact
    assert res.json[
        "outcome_of_contact"] == example_complaint.outcome_of_contact
    assert res.json[
        "incident_date"] == example_complaint.incident_date.isoformat()
    assert res.json[
        "received_date"] == example_complaint.received_date.isoformat()
    assert res.json[
        "closed_date"] == example_complaint.closed_date.isoformat()

    for prop, value in res.json['location'][0].items():
        assert getattr(example_complaint.location.single(), prop) == value

    for prop, value in res.json['allegations'][0].items():
        assert getattr(example_complaint.allegations.single(), prop) == value

    for prop, value in res.json['penalties'][0].items():
        if prop == "date_assessed":
            assert getattr(
                example_complaint.penalties.single(),
                prop
            ).isoformat() == value
        else:
            assert getattr(
                example_complaint.penalties.single(), prop) == value


def test_get_complaints(client, db_session, access_token, example_complaint):
    all_complaints = Complaint.nodes.all()
    res = client.get(
        "/api/v1/complaints/",
        headers={"Authorization ": "Bearer {0}".format(access_token)},
    )

    assert res.status_code == 200
    assert res.json["total"] == len(all_complaints)
    assert res.json["page"] == 1
    assert len(res.json["results"]) == len(all_complaints)


def test_complaint_pagination(
        client, db_session, access_token, example_complaint):
    # Create Complaints in the database
    complaints = Complaint.nodes.all()
    per_page = 1
    expected_total_pages = math.ceil(len(complaints)//per_page)

    for page in range(1, expected_total_pages + 1):
        res = client.get(
            "/api/v1/complaints/",
            query_string={"per_page": per_page, "page": page},
            headers={"Authorization": "Bearer {0}".format(access_token)},
        )

        assert res.status_code == 200
        assert res.json["page"] == page
        assert res.json["total"] == len(complaints)
        assert len(res.json["results"]) == per_page

    res = client.get(
        "/api/v1/complaints/",
        query_string={"perPage": per_page, "page": expected_total_pages + 1},
        headers={"Authorization": "Bearer {0}".format(access_token)},
    )
    assert res.status_code == 404


def test_update_complaint(
        client, db_session, example_source, example_contributor,
        contributor_access_token, example_complaint):
    """Test that we can update an existing complaint."""
    update = {
        "reason_for_contact": "Updated reason for contact",
        "outcome_of_contact": "Updated outcome of contact",
    }

    res = client.patch(
        f"/api/v1/complaints/{example_complaint.uid}",
        json=update,
        headers={"Authorization": f"Bearer {contributor_access_token}"},
    )

    assert res.status_code == 200
    response = res.json

    assert response["uid"] == example_complaint.uid
    assert response["reason_for_contact"] == update["reason_for_contact"]
    assert response["outcome_of_contact"] == update["outcome_of_contact"]

    # Verify the database is updated
    c = Complaint.nodes.get(uid=example_complaint.uid)
    assert c.reason_for_contact == update["reason_for_contact"]
    assert c.outcome_of_contact == update["outcome_of_contact"]


def test_update_complaint_no_edit_permission(
        client, access_token, example_complaint):
    # Verify that a user without edit permissions cannot update
    res = client.patch(
        f"/api/v1/complaints/{example_complaint.uid}",
        json={"incident_date": "2023-01-01"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 403


def test_delete_complaint(
        client, db_session, access_token,
        p_admin_access_token, example_complaint):
    """Test that we can delete an existing complaint."""
    res = client.delete(
        f"/api/v1/complaints/{example_complaint.uid}",
        headers={"Authorization": f"Bearer {p_admin_access_token}"},
    )

    assert res.status_code == 204

    # Verify the complaint is deleted
    with pytest.raises(Complaint.DoesNotExist):
        Complaint.nodes.get(uid=example_complaint.uid)


def test_get_allegations(client, db_session, example_complaint, access_token):
    """Test that we can retrieve allegations associated with a complaint."""
    res = client.get(
        f"/api/v1/complaints/{example_complaint.uid}/allegations",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    allegation_objs = example_complaint.allegations.all()
    allegations = res.json["results"]

    assert res.status_code == 200
    assert res.json["total"] == len(allegation_objs)
    assert res.json["page"] == 1
    assert allegations[0]["allegation"] == allegation_objs[0].allegation
    assert allegations[0]["type"] == allegation_objs[0].type


def test_get_penalties(client, db_session, example_complaint, access_token):
    """Test that we can retrieve penalties associated with a complaint."""
    res = client.get(
        f"/api/v1/complaints/{example_complaint.uid}/penalties",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    penalty_objs = example_complaint.penalties.all()
    penalties = res.json["results"]

    assert res.status_code == 200
    assert res.json["total"] == len(penalty_objs)
    assert res.json["page"] == 1
    p = example_complaint.penalties.single()
    assert penalties[0]["penalty"] == p.penalty
    assert penalties[0]["date_assessed"] == p.date_assessed.isoformat()


def test_get_investigations(
        client, db_session, example_complaint, access_token):
    """Test that we can retrieve investigations
    associated with a complaint."""
    res = client.get(
        f"/api/v1/complaints/{example_complaint.uid}/investigations",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    investigation_objs = example_complaint.investigations.all()
    investigations = res.json["results"]

    assert res.status_code == 200
    assert res.json["total"] == len(investigation_objs)
    assert res.json["page"] == 1
    i = example_complaint.investigations.single()
    assert investigations[0]["start_date"] == i.start_date.isoformat()
    assert investigations[0]["end_date"] == i.end_date.isoformat()

# def test_update_complaint_children(
# client, db_session, contributor_access_token, example_complaint):
    # """Test that we can update the children of an existing complaint."""
    # updated_data = {
    #     "allegations": [
    #         {
    #             "allegation": "Updated allegation",
    #             "type": "Updated type"
    #         }
    #     ],
    #     "penalties": [
    #         {
    #             "penalty": "Updated penalty",
    #             "date_assessed": "2022-01-01"
    #         }
    #     ],
    #     "investigations": [
    #         {
    #             "start_date": "2022-01-01",
    #             "end_date": "2022-01-02"
    #         }
    #     ]
    # }

    # res = client.put(
    #     f"/api/v1/complaints/{example_complaint.uid}",
    #     json=updated_data,
    #     headers={"Authorization": f"Bearer {contributor_access_token}"},
    # )

    # assert res.status_code == 200
    # response = res.json

    # assert response["allegations"] == updated_data["allegations"]
    # assert response["penalties"] == updated_data["penalties"]
    # assert response["investigations"] == updated_data["investigations"]

    # # Verify the database is updated
    # complaint_obj = Complaint.nodes.get(uid=example_complaint.uid)
    # assert complaint_obj.allegations == updated_data["allegations"]
    # assert complaint_obj.penalties == updated_data["penalties"]
    # assert complaint_obj.investigations == updated_data["investigations"]
