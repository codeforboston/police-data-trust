from __future__ import annotations
import pytest
from datetime import datetime, date
import math
from backend.database import (
    Complaint, Source, Officer, Location, RecordType,
    Allegation, Civilian, Investigation, Penalty
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


@pytest.fixture
def example_complaints(db_session, example_source, example_officer):
    complaints = []
    source_rel = {
        "record_type": RecordType.government.value,
        "reporting_agency": "New York City Civilian Review Board",
        "reporting_agency_url": "https://www.nyc.gov/site/crb/index.page",
        "reporting_agency_email": "example@example.com",
        "date_published": datetime.now()
    }
    for i in range(3):
        c = Complaint(
            record_id=f"2022027{i}",
            category=mock_complaint["category"],
            reason_for_contact=mock_complaint["reason_for_contact"],
            outcome_of_contact=mock_complaint["outcome_of_contact"],
            incident_date=date.fromisoformat(
                mock_complaint["incident_date"]),
            received_date=date.fromisoformat(
                mock_complaint["received_date"]),
            closed_date=date.fromisoformat(
                mock_complaint["closed_date"]),
        ).save()
        c.source_org.connect(
            example_source, source_rel)
        loc = Location(**mock_complaint["location"]).save()
        allege = Allegation(
            allegation=mock_complaint["allegations"][0]["allegation"],
            type=mock_complaint["allegations"][0]["type"],
            finding=mock_complaint["allegations"][0]["finding"],
            outcome=mock_complaint["allegations"][0]["outcome"]
        ).save()
        civ = Civilian(**mock_complaint["allegations"][0]["complainant"]).save()
        allege.complainant.connect(civ)
        allege.accused.connect(example_officer)
        allege.complaint.connect(c)
        c.location.connect(loc)
        complaints.append(c)
    return complaints


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
    allegation_obj = c.allegations.first()
    complainant_obj = allegation_obj.complainant.single()
    penalty_obj = c.penalties.first()

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
        client, access_token, example_source):

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
        assert getattr(example_complaint.allegations.first(), prop) == value

    for prop, value in res.json['penalties'][0].items():
        if prop == "date_assessed":
            assert getattr(
                example_complaint.penalties.first(),
                prop
            ).isoformat() == value
        else:
            assert getattr(
                example_complaint.penalties.first(), prop) == value


def test_get_complaints(client, db_session, access_token, example_complaints):
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
        client, db_session, access_token, example_complaints):
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


def test_delete_complaint_no_permission(
        client, db_session, access_token,
        contributor_access_token, example_complaint):
    # Verify that a user without delete permissions cannot delete
    res = client.delete(
        f"/api/v1/complaints/{example_complaint.uid}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 403

    res = client.delete(
        f"/api/v1/complaints/{example_complaint.uid}",
        headers={"Authorization": f"Bearer {contributor_access_token}"},
    )
    assert res.status_code == 403


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


def test_create_allegation(
    client, db_session, contributor_access_token,
    example_complaint, example_officer
):
    """Test that we can create an allegation for a complaint."""
    new_allegation = {
        "allegation": "New allegation",
        "type": "New type",
        "accused_uid": example_officer.uid
    }

    res = client.post(
        f"/api/v1/complaints/{example_complaint.uid}/allegations",
        json=new_allegation,
        headers={"Authorization": f"Bearer {contributor_access_token}"},
    )

    assert res.status_code == 201
    response = res.json

    assert response["allegation"] == new_allegation["allegation"]
    assert response["type"] == new_allegation["type"]

    # Verify the database is updated
    complaint_obj = Complaint.nodes.get(uid=example_complaint.uid)
    a_obj = Allegation.nodes.get(uid=response["uid"])
    assert a_obj.complaint.is_connected(complaint_obj)
    assert a_obj.allegation == new_allegation["allegation"]
    assert a_obj.type == new_allegation["type"]
    assert a_obj.accused.single().uid == new_allegation["accused_uid"]


def test_update_allegation(
    client, db_session, contributor_access_token, example_complaint
):
    """Test that we can update the allegation of an existing complaint."""
    updated_data = {
        "allegation": "Updated allegation",
        "type": "Updated type"
    }

    a = example_complaint.allegations.first()

    res = client.patch(
        f"/api/v1/complaints/{example_complaint.uid}/allegations/{a.uid}",
        json=updated_data,
        headers={"Authorization": f"Bearer {contributor_access_token}"},
    )

    assert res.status_code == 200
    response = res.json

    assert response["allegation"] == updated_data["allegation"]
    assert response["type"] == updated_data["type"]

    # Verify the database is updated
    complaint_obj = Complaint.nodes.get(uid=example_complaint.uid)
    a_obj = complaint_obj.allegations.first()
    assert a_obj.allegation == updated_data["allegation"]
    assert a_obj.type == updated_data["type"]

    res = client.delete(
        f"/api/v1/complaints/{example_complaint.uid}/allegations/{a.uid}",
        headers={"Authorization": f"Bearer {contributor_access_token}"},
    )
    assert res.status_code == 204
    assert not a_obj.complaint.is_connected(complaint_obj)


def test_update_allegation_no_permission(
    client, access_token, example_complaint
):
    """Test that a user without edit permissions cannot update an allegation."""
    a = example_complaint.allegations.first()

    res = client.patch(
        f"/api/v1/complaints/{example_complaint.uid}/allegations/{a.uid}",
        json={"allegation": "Unauthorized update"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 403

    res = client.delete(
        f"/api/v1/complaints/{example_complaint.uid}/allegations/{a.uid}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 403


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
    p = example_complaint.penalties.first()
    assert penalties[0]["penalty"] == p.penalty
    assert penalties[0]["date_assessed"] == p.date_assessed.isoformat()


def test_create_penalty(
    client, db_session, contributor_access_token,
    example_complaint, example_officer
):
    """Test that we can create a penalty for a complaint."""
    new_penalty = {
        "penalty": "New penalty",
        "date_assessed": "2023-01-01",
        "officer_uid": example_officer.uid
    }

    res = client.post(
        f"/api/v1/complaints/{example_complaint.uid}/penalties",
        json=new_penalty,
        headers={"Authorization": f"Bearer {contributor_access_token}"},
    )

    assert res.status_code == 201
    response = res.json

    assert response["penalty"] == new_penalty["penalty"]
    assert response["date_assessed"] == new_penalty["date_assessed"]

    # Verify the database is updated
    complaint_obj = Complaint.nodes.get(uid=example_complaint.uid)
    p_obj = Penalty.nodes.get(uid=response["uid"])
    assert p_obj.complaint.is_connected(complaint_obj)
    assert p_obj.penalty == new_penalty["penalty"]
    assert p_obj.date_assessed == date.fromisoformat(
        new_penalty["date_assessed"])


def test_update_penalty(
    client, db_session, contributor_access_token, example_complaint
):
    """Test that we can update the penalty of an existing complaint."""
    updated_data = {
        "penalty": "Updated penalty",
        "date_assessed": "2023-01-02"
    }

    p = example_complaint.penalties.first()

    res = client.patch(
        f"/api/v1/complaints/{example_complaint.uid}/penalties/{p.uid}",
        json=updated_data,
        headers={"Authorization": f"Bearer {contributor_access_token}"},
    )

    assert res.status_code == 200
    response = res.json

    assert response["penalty"] == updated_data["penalty"]
    assert response["date_assessed"] == updated_data["date_assessed"]

    # Verify the database is updated
    complaint_obj = Complaint.nodes.get(uid=example_complaint.uid)
    p_obj = complaint_obj.penalties.first()
    assert p_obj.penalty == updated_data["penalty"]
    assert p_obj.date_assessed == date.fromisoformat(
        updated_data["date_assessed"])

    res = client.delete(
        f"/api/v1/complaints/{example_complaint.uid}/penalties/{p.uid}",
        headers={"Authorization": f"Bearer {contributor_access_token}"},
    )
    assert res.status_code == 204
    assert not p_obj.complaint.is_connected(complaint_obj)


def test_update_penalty_no_permission(
    client, access_token, example_complaint
):
    """Test that a user without edit permissions cannot update a penalty."""
    p = example_complaint.penalties.first()

    res = client.patch(
        f"/api/v1/complaints/{example_complaint.uid}/penalties/{p.uid}",
        json={"penalty": "Unauthorized update"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 403

    res = client.delete(
        f"/api/v1/complaints/{example_complaint.uid}/penalties/{p.uid}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 403


def test_get_investigations(
    client, db_session, example_complaint, access_token
):
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
    i = example_complaint.investigations.first()
    assert investigations[0]["start_date"] == i.start_date.isoformat()
    assert investigations[0]["end_date"] == i.end_date.isoformat()


def test_create_investigation(
    client, db_session, contributor_access_token,
    example_complaint, example_officer
):
    """Test that we can create an allegation for a complaint."""
    new_investigation = {
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "investigator_uid": example_officer.uid
    }

    res = client.post(
        f"/api/v1/complaints/{example_complaint.uid}/investigations",
        json=new_investigation,
        headers={"Authorization": f"Bearer {contributor_access_token}"},
    )

    assert res.status_code == 201
    response = res.json

    assert response["start_date"] == new_investigation["start_date"]
    assert response["end_date"] == new_investigation["end_date"]

    # Verify the database is updated
    complaint_obj = Complaint.nodes.get(uid=example_complaint.uid)
    i_obj = Investigation.nodes.get(uid=response["uid"])
    assert i_obj.complaint.is_connected(complaint_obj)
    assert i_obj.start_date == date.fromisoformat(
        new_investigation["start_date"])
    assert i_obj.end_date == date.fromisoformat(
        new_investigation["end_date"])


def test_update_investigation(
    client, db_session, contributor_access_token, example_complaint
):
    """Test that we can update the investigation of an existing complaint."""
    updated_data = {
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    }

    i = example_complaint.investigations.first()

    res = client.patch(
        f"/api/v1/complaints/{example_complaint.uid}/investigations/{i.uid}",
        json=updated_data,
        headers={"Authorization": f"Bearer {contributor_access_token}"},
    )

    assert res.status_code == 200
    response = res.json

    assert response["start_date"] == updated_data["start_date"]
    assert response["end_date"] == updated_data["end_date"]

    # Verify the database is updated
    complaint_obj = Complaint.nodes.get(uid=example_complaint.uid)
    i_obj = complaint_obj.investigations.first()
    assert i_obj.start_date == date.fromisoformat(updated_data["start_date"])
    assert i_obj.end_date == date.fromisoformat(updated_data["end_date"])

    res = client.delete(
        f"/api/v1/complaints/{example_complaint.uid}/investigations/{i.uid}",
        headers={"Authorization": f"Bearer {contributor_access_token}"},
    )
    assert res.status_code == 204
    assert not i_obj.complaint.is_connected(complaint_obj)


def test_update_investigation_no_permission(
    client, access_token, example_complaint
):
    """Test that a user without edit permissions
    cannot update an investigation."""
    i = example_complaint.investigations.first()

    res = client.patch(
        f"/api/v1/complaints/{example_complaint.uid}/investigations/{i.uid}",
        json={
            "start_date": "Unauthorized update",
            "end_date": "Unauthorized update"
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 403

    res = client.delete(
        f"/api/v1/complaints/{example_complaint.uid}/investigations/{i.uid}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == 403


def test_create_allegation_with_civilian(
    client, db_session, contributor_access_token,
    example_complaint, example_officer
):
    """Test create an allegation with civilian info"""
    new_allegation = {
        "accused_uid": example_officer.uid,
        "complainant": {
            "age": 37,
            "age_range": "35-39",
            "ethnicity": None,
            "gender": "Male"
        },
        "allegation": "Refusal to process civilian complaint",
        "type": "Abuse of Authority"
        }

    complaint = Complaint.nodes.get(uid=example_complaint.uid)
    civ_count_before = len(complaint.complainants.all())
    assert civ_count_before == 0

    res = client.post(
        f"/api/v1/complaints/{example_complaint.uid}/allegations",
        json=new_allegation,
        headers={"Authorization": f"Bearer {contributor_access_token}"},
    )

    assert res.status_code == 201
    response = res.json

    assert response["allegation"] == new_allegation["allegation"]
    assert response["type"] == new_allegation["type"]

    # Verify the database is updated
    a_obj = Allegation.nodes.get(uid=response["uid"])
    assert a_obj.complaint.is_connected(complaint)
    assert a_obj.allegation == new_allegation["allegation"]
    assert a_obj.type == new_allegation["type"]
    assert a_obj.accused.single().uid == new_allegation["accused_uid"]
    civ = a_obj.complainant.single()
    assert civ.civ_id is not None
    civ_count_after = len(complaint.complainants.all())
    assert civ_count_after == civ_count_before + 1


def test_create_allegations_with_same_civilian(
    client, db_session, contributor_access_token,
    example_complaint, example_officer
):
    """Test create multiple allegations using same civilian"""
    first_allegation = mock_complaint["allegations"][0].copy()
    first_allegation["accused_uid"] = example_officer.uid

    complaint = Complaint.nodes.get(uid=example_complaint.uid)
    civ_count_before = len(complaint.complainants.all())
    assert civ_count_before == 0

    res = client.post(
        f"/api/v1/complaints/{example_complaint.uid}/allegations",
        json=first_allegation,
        headers={"Authorization": f"Bearer {contributor_access_token}"},
    )

    assert res.status_code == 201
    response = res.json

    a_obj = Allegation.nodes.get(uid=response["uid"])
    # check new civilian was created
    civ_count_after = len(complaint.complainants.all())
    assert civ_count_after == 1
    civ = a_obj.complainant.single()
    assert civ.civ_id == f"{complaint.uid}-{civ_count_after}"
    print("pytest CIV ID:", civ.civ_id)

    second_allegation = first_allegation.copy()
    # use existing civilian
    second_allegation["complainant"]["complainant_id"] = civ.civ_id

    res = client.post(
        f"/api/v1/complaints/{example_complaint.uid}/allegations",
        json=second_allegation,
        headers={"Authorization": f"Bearer {contributor_access_token}"},
    )

    assert res.status_code == 201
    response = res.json

    # check new civilian was NOT created
    a_obj = Allegation.nodes.get(uid=response["uid"])
    civ_count_after = len(complaint.complainants.all())
    assert civ_count_after == 1
    civ = a_obj.complainant.single()
    assert civ.civ_id == f"{complaint.uid}-{civ_count_after}"
