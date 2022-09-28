# flake8: noqa: F401
from backend.database.core import db
from backend.database.core import db_cli
from backend.database.core import execute_query

# TODO: remove star imports; at the moment it is a convenience to make sure
#  that all db models are loaded into the SQLAlchemy metadata.

# NOTE: We are deliberately _not_ loading all the models. The reason why is
#  because we want to do baby steps-- one model at a time. This ensures that
#  Alembic only does a couple models, not all of them.

from .models.agency import *
from .models.attorney import *
from .models.case_document import *
from .models.incident import *
from .models.investigation import *
from .models.legal_case import *
from .models.multimedia import *
from .models.officer import *
from .models.participant import *
from .models.tag import *
from .models.result_of_stop import *
from .models.action import *
from .models.use_of_force import *
from .models.user import *
from .models.victim import *
from .models.accusation import *
from .models.source import *
