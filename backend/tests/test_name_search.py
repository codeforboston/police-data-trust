"""Name search ranking, and search text that must never break a query."""
from datetime import date, datetime

import pytest
from neomodel import db

from backend.database import Agency, Employment, Jurisdiction, Officer
from backend.queries.text_search import (
    build_all_words_query,
    build_exact_query,
    build_prefix_query,
    tokenize,
)

# Officers in Example Agency's Precinct 1: (first, middle, last, rank).
PEOPLE = {
    "Anthony Rivera": ("Anthony", None, "Rivera", "Detective"),
    "Marcus Anthony Rivera": ("Marcus", "Anthony", "Rivera", "Police Officer"),
    "Antonio Rivas": ("Antonio", None, "Rivas", "Police Officer"),
    "Anthony Smith": ("Anthony", None, "Smith", "Police Officer"),
    "Jose Rivera": ("Jose", None, "Rivera", "Police Officer"),
    "Kevin O'Brien": ("Kevin", None, "O'Brien", "Sergeant"),
}


def refresh_fulltext_indexes():
    db.cypher_query(
        "CALL db.index.fulltext.awaitEventuallyConsistentIndexRefresh()")


@pytest.fixture
def named_officers(example_source, example_unit, add_test_change):
    officers = {}
    for key, (first, middle, last, rank) in PEOPLE.items():
        officer = Officer(
            first_name=first, middle_name=middle, last_name=last).save()
        add_test_change(officer, example_source, timestamp=datetime.now())
        employment = Employment(
            highest_rank=rank, earliest_date=date(2020, 1, 1)).save()
        employment.unit.connect(example_unit)
        employment.officer.connect(officer)
        officers[key] = officer
    refresh_fulltext_indexes()
    return officers


def get(client, access_token, path, **params):
    return client.get(
        path,
        query_string={"per_page": 50, **params},
        headers={"Authorization": f"Bearer {access_token}"},
    )


def result_names(res) -> list[str]:
    """The names shown for a page of results, whichever endpoint sent it."""
    assert res.status_code == 200, res.data[:300]
    names = []
    for item in res.json["results"]:
        if item.get("title"):
            names.append(item["title"])
            continue
        officer = item.get("officer", item)
        names.append(" ".join(
            officer[part] for part in ("first_name", "middle_name", "last_name")
            if officer.get(part)))
    return names


# ---- direct matches first, partial matches after ------------------------

@pytest.mark.parametrize("term", ["Anthony Rivera", "Rivera Anthony"])
def test_officer_search_ranks_direct_matches_first(
        client, access_token, named_officers, term):
    names = result_names(get(
        client, access_token, "/api/v1/officers",
        term=term, searchResult="true"))

    # An exact first and last name, in either order, comes first; then a
    # name holding both words (here through the middle name).
    assert names[:2] == ["Anthony Rivera", "Marcus Anthony Rivera"]
    # Partial matches are still listed, below the direct ones.
    assert set(names[2:]) == {"Anthony Smith", "Jose Rivera"}


def test_officer_search_matches_the_start_of_words(
        client, access_token, named_officers):
    names = result_names(get(
        client, access_token, "/api/v1/officers",
        term="Ant Riv", searchResult="true"))

    assert set(names[:3]) == {
        "Anthony Rivera", "Marcus Anthony Rivera", "Antonio Rivas"}
    assert set(names[3:]) == {"Anthony Smith", "Jose Rivera"}


def test_separate_name_fields_still_require_every_word(
        client, access_token, named_officers):
    names = result_names(get(
        client, access_token, "/api/v1/officers",
        first_name="Anthony", last_name="Rivera", searchResult="true"))

    assert names == ["Anthony Rivera", "Marcus Anthony Rivera"]


def test_all_tab_ranks_officers_agencies_and_units(
        client, access_token, named_officers, example_agency):
    names = result_names(get(
        client, access_token, "/api/v1/search", term="Rivera Anthony"))
    assert names[:2] == ["Anthony Rivera", "Marcus Anthony Rivera"]

    for name in ("Houston Police Department", "Austin Police Department"):
        Agency(name=name, hq_state="TX",
               jurisdiction=Jurisdiction.MUNICIPAL.value).save()
    refresh_fulltext_indexes()

    names = result_names(get(
        client, access_token, "/api/v1/search", term="Houston Police"))
    assert names[0] == "Houston Police Department"
    assert "Austin Police Department" in names[1:]


def test_agency_search_ranks_direct_matches_first(client, access_token):
    for name in ("Fort Bend County Constable", "Harris County Constable",
                 "Harris County Precinct"):
        Agency(name=name, hq_state="TX",
               jurisdiction=Jurisdiction.MUNICIPAL.value).save()
    refresh_fulltext_indexes()

    res = get(client, access_token, "/api/v1/agencies", term="Harris County")
    assert res.status_code == 200
    names = [agency["name"] for agency in res.json["results"]]

    assert set(names[:2]) == {
        "Harris County Constable", "Harris County Precinct"}
    assert names[2:] == ["Fort Bend County Constable"]


def test_agency_and_unit_officer_lists_rank_direct_matches_first(
        client, access_token, named_officers, example_agency, example_unit):
    for path in (f"/api/v1/agencies/{example_agency.uid}/officers",
                 f"/api/v1/units/{example_unit.uid}/officers"):
        names = result_names(get(
            client, access_token, path, term="Rivera Anthony"))

        assert names[:2] == ["Anthony Rivera", "Marcus Anthony Rivera"]
        assert set(names[2:]) == {"Anthony Smith", "Jose Rivera"}


# ---- search text never breaks a query -----------------------------------

@pytest.mark.parametrize(
    "term", ["O'Brien", "Rivera (", '"Rivera', "Rivera') //", "AND Rivera"])
def test_search_text_with_query_syntax_is_handled(
        client, access_token, named_officers, example_agency, example_unit,
        term):
    searches = [
        ("/api/v1/officers", {"term": term, "searchResult": "true"}),
        ("/api/v1/officers", {"rank": term}),
        ("/api/v1/search", {"term": term}),
        ("/api/v1/agencies", {"term": term}),
        ("/api/v1/units", {"name": term}),
        (f"/api/v1/agencies/{example_agency.uid}/officers", {"term": term}),
        (f"/api/v1/units/{example_unit.uid}/officers", {"term": term}),
    ]
    for path, params in searches:
        res = get(client, access_token, path, **params)
        assert res.status_code == 200, (path, params, res.data[:300])

    assert len(Officer.nodes.all()) == len(PEOPLE)


def test_officer_search_finds_names_with_apostrophes(
        client, access_token, named_officers):
    names = result_names(get(
        client, access_token, "/api/v1/officers",
        term="O'Brien", searchResult="true"))

    assert names == ["Kevin O'Brien"]


def test_rank_search_returns_only_that_rank(
        client, access_token, named_officers):
    for rank in ("Detective", "Detective'"):
        res = get(client, access_token, "/api/v1/officers", rank=rank)

        assert res.status_code == 200
        assert [o["uid"] for o in res.json["results"]] == [
            named_officers["Anthony Rivera"].uid]


def test_search_text_with_nothing_searchable(
        client, access_token, named_officers):
    res = get(client, access_token, "/api/v1/search", term="( AND )")
    assert res.status_code == 400

    res = get(client, access_token, "/api/v1/officers",
              term="( AND )", searchResult="true")
    assert res.status_code == 200
    assert res.json == {"message": "No results found matching the query"}


# ---- helpers ---------------------------------------------------------------

def test_tokenize_splits_name_punctuation_but_keeps_apostrophes():
    assert tokenize("Rivera, Anthony J. O'Brien-Smith AND (x)") == [
        "rivera", "anthony", "j", "o'brien", "smith", "x"]


def test_build_prefix_query_rejects_text_with_nothing_searchable():
    with pytest.raises(ValueError, match="Query parameter is required"):
        build_prefix_query("( AND )")


def test_build_all_words_query_requires_every_word():
    assert build_all_words_query("John AND Doe-Smith") == "+john +doe +smith"


def test_build_exact_query_escapes_lucene_syntax():
    assert build_exact_query('Detective" (2nd) AND 12-3') == (
        'Detective\\" \\(2nd\\) 12\\-3')
