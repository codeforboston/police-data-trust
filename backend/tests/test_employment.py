import pytest
from backend.database import Agency, Officer


mock_officers = {
    "john": {
        "first_name": "John",
        "last_name": "Doe",
        "race": "White",
        "ethnicity": "Non-Hispanic",
        "gender": "M"
    },
    "hazel": {
        "first_name": "Hazel",
        "last_name": "Nutt",
        "race": "White",
        "ethnicity": "Non-Hispanic",
        "gender": "F"
    },
    "frank": {
        "first_name": "Frank",
        "last_name": "Furter",
        "race": "Black",
        "ethnicity": "African American",
        "gender": "M"
    }
}
mock_agencies = {
    "cpd": {
        "name": "Chicago Police Department",
        "website_url": "https://www.chicagopolice.org/",
        "hq_address": "3510 S Michigan Ave",
        "hq_city": "Chicago",
        "hq_zip": "60653",
        "jurisdiction": "MUNICIPAL"
    },
    "nypd": {
        "name": "New York Police Department",
        "website_url": "https://www1.nyc.gov/site/nypd/index.page",
        "hq_address": "1 Police Plaza",
        "hq_city": "New York",
        "hq_zip": "10038",
        "jurisdiction": "MUNICIPAL"
    }
}

mock_add_officers = {
    "john": {
        "earliest_employment": "2015-03-14 00:00:00",
        "badge_number": "1234",
        "currently_employed": True
    },
    "hazel": {
        "earliest_employment": "2018-08-12 00:00:00",
        "badge_number": "5678",
        "currently_employed": True
    },
    "frank": {
        "earliest_employment": "2019-05-03 00:00:00",
        "badge_number": "1234",
        "currently_employed": True
    }
}

mock_add_history = {
    "nypd": {
        "earliest_employment": "2015-03-14 00:00:00",
        "latest_employment": "2018-08-12 00:00:00",
        "badge_number": "1234",
    },
    "cpd": {
        "earliest_employment": "2018-08-12 00:00:00",
        "latest_employment": "2019-05-03 00:00:00",
        "badge_number": "5678",
    }
}


@pytest.fixture
def example_agencies(db_session):
    agencies = {}

    for name, mock in mock_agencies.items():
        db_session.add(Agency(**mock))
        db_session.commit()
        agencies[name] = db_session.query(
            Agency).filter(Agency.name == mock["name"]).first()

    db_session.commit()
    return agencies

@pytest.fixture
def example_officers(db_session):
    officers = {}
    for name, mock in mock_officers.items():
        o = Officer(**mock)
        o.create()
        officers[name] = o
    db_session.commit()
    return officers


def test_add_officers_to_agency(
        db_session,
        client,
        example_agency,
        example_officers,
        contributor_access_token):
    agency = example_agency
    officers = example_officers
    records = []
    for name, mock in mock_add_officers.items():
        mock["officer_id"] = officers[name].id
        records.append(mock)

    res = client.post(
        f"/api/v1/agencies/{agency.id}/officers",
        json={"officers": records},
        headers={"Authorization": f"Bearer {contributor_access_token}"}
    )
    assert res.status_code == 200
    assert len(res.json["created"]) == len(records)
    assert len(res.json["failed"]) == 0


def test_add_history_to_officer(
        db_session,
        client,
        example_agencies,
        example_officer,
        contributor_access_token):
    records = []
    for name, mock in mock_add_history.items():
        mock["agency_id"] = example_agencies[name].id
        records.append(mock)

    res = client.put(
        f"/api/v1/officers/{example_officer.id}/employment",
        json={"agencies": records},
        headers={"Authorization": f"Bearer {contributor_access_token}"}
    )
    assert res.status_code == 200
    assert len(res.json["created"]) == len(records)
    assert len(res.json["failed"]) == 0
