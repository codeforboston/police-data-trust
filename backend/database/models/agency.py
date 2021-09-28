from .. import db

# TODO agency model


class AgencyAtIncident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
