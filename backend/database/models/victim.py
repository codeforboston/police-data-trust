from .. import db
from .types.enums import Race
from .types.enums import Gender


class Victim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    race = db.Column(db.Enum(Race))
    gender = db.Column(db.Enum(Gender))
    date_of_birth = db.Column(db.Date)  # TODO: add "estimated"?
    manner_of_injury = db.Column(db.Text)  # TODO: is an enum
    # TODO: deceased is better as calculated value; if time of death is null.
    deceased = db.Column(db.Boolean)
    time_of_death = db.Column(db.DateTime, nullable=True)
