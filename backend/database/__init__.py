# flake8: noqa: F401
from backend.database.core import db, db_cli, execute_query

# Neo4j / NeoModel related imports
from neomodel import config as neo_config

# TODO: remove star imports; at the moment it is a convenience to make sure
#  that all db models are loaded into the SQLAlchemy metadata.

# NOTE: We are deliberately _not_ loading all the models. The reason why is
#  because we want to do baby steps-- one model at a time. This ensures that
#  Alembic only does a couple models, not all of them.

# Neomodel models
from .models.officer import *
from .models.agency import *
from .models.complaint import *
from .models.litigation import *
from .models.attachment import *
from .models.civilian import *
from .models.user import *
from .models.partner import *
