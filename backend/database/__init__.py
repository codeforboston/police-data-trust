# flake8: noqa: F401
from .core import db
from .core import migrate
from .core import db_cli
from .core import execute_query

# TODO: remove star imports; at the moment it is a convenience to make sure
#  that all db models are loaded into the SQLAlchemy metadata.
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
from .models.users import *
from .models.victim import *
