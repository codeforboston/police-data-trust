import enum
from .. import db, CrudMixin


class Rank(int, enum.Enum):
    # TODO: Is this comprehensive?
    TECHNICIAN = 10
    OFFICER = 20
    DETECTIVE = 30
    CORPORAL = 40
    SERGEANT = 50
    LIEUTENANT = 60
    CAPTAIN = 70
    DEPUTY = 80
    CHIEF = 90
    COMMISSIONER = 100


class Employment(db.Model, CrudMixin):
    id = db.Column(db.Integer, primary_key=True)
    officer_id = db.Column(db.Integer, db.ForeignKey("officer.id"))
    agency_id = db.Column(db.Integer, db.ForeignKey("agency.id"))
    unit_id = db.Column(db.Integer, db.ForeignKey("unit.id"))
    earliest_employment = db.Column(db.Text)
    latest_employment = db.Column(db.Text)
    badge_number = db.Column(db.Text)
    highest_rank = db.Column(db.Enum(Rank))
    currently_employed = db.Column(db.Boolean)

    officer = db.relationship("Officer", back_populates="agency_association")
    agency = db.relationship("Agency", back_populates="officer_association")
    unit = db.relationship("Unit", backref="unit_association")

    def __repr__(self):
        return f"<Employment {self.id}>"


def get_employment_range(records: list[Employment]):
    earliest_employment = None
    latest_employment = None

    for record in records:
        if record.earliest_employment is not None:
            if earliest_employment is None:
                earliest_employment = record.earliest_employment
            elif record.earliest_employment < earliest_employment:
                earliest_employment = record.earliest_employment
        if record.latest_employment is not None:
            if latest_employment is None:
                latest_employment = record.latest_employment
            elif record.latest_employment > latest_employment:
                latest_employment = record.latest_employment
    return earliest_employment, latest_employment


def get_highest_rank(records: list[Employment]):
    highest_rank = None
    for record in records:
        if record.highest_rank is not None:
            if highest_rank is None:
                highest_rank = record.highest_rank
            elif record.highest_rank > highest_rank:
                highest_rank = record.highest_rank
    return highest_rank


def merge_employment_records(
        records: list[Employment],
        currently_employed: bool = None
        ):
    """
    Merge employment records for a single officer
    and agency into a single record.
    Args:
        records (list[Employment]): List of Employment records
            for a single officer
        badge_number (str, optional): Badge number. Defaults to None.
        unit (str, optional): Unit. Defaults to None.
    Returns:
        Employment: A single Employment record. If no unit, or
        currently_employed is provided, they will take the value of the
        first record in the list.
        The agency_id, officer_id, and badge_number will always be taken from
        the first record in the list.
    """
    earliest_employment, latest_employment = get_employment_range(records)
    highest_rank = get_highest_rank(records)
    if currently_employed is None:
        currently_employed = records[0].currently_employed
    return Employment(
        officer_id=records[0].officer_id,
        agency_id=records[0].agency_id,
        badge_number=records[0].badge_number,
        earliest_employment=earliest_employment,
        latest_employment=latest_employment,
        unit=records[0].unit_id,
        highest_rank=highest_rank,
        currently_employed=currently_employed,
    )
