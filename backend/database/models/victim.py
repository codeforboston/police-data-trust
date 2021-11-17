from .. import db


class Victim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_id = db.Column(db.Integer, db.ForeignKey("incident.id"))
    name = db.Column(db.Text)
    race = db.Column(db.Text)
    gender = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)  # TODO: add "estimated"?
    manner_of_injury = db.Column(db.Text)  # TODO: is an enum
    injury_description = db.Column(db.Text)
    injury_condition = db.Column(db.Text)
    # TODO: deceased is better as calculated value; if time of death is null.
    deceased = db.Column(db.Boolean)
    time_of_death = db.Column(db.DateTime, nullable=True)
