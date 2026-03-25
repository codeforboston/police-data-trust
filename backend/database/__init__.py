# flake8: noqa: F401
import inspect
import pkgutil
import importlib
from backend.database.core import db_cli
from neomodel import StructuredNode, config as neo_config

# Collect all models in the database package
import backend.database.models as _models_pkg

MODEL_CLASSES = []
for _finder, module_name, _ispkg in pkgutil.iter_modules(_models_pkg.__path__):
    module = importlib.import_module(f"{_models_pkg.__name__}.{module_name}")
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if (
            issubclass(obj, StructuredNode)
            and obj.__module__.startswith("backend.database.models")
            and obj is not StructuredNode
        ):
            MODEL_CLASSES.append(obj)


MODEL_NAMES = [cls.__name__ for cls in MODEL_CLASSES]


# Neomodel models
from .models.officer import *
from .models.agency import *
from .models.employment import *
from .models.complaint import *
from .models.litigation import *
from .models.attachment import *
from .models.civilian import *
from .models.user import *
from .models.source import *
from .models.contact import *
