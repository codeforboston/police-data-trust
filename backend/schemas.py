from __future__ import annotations
import json
import textwrap
from functools import wraps
from enum import Enum
from collections import OrderedDict
from typing import Any, Optional, TypeVar, Type, List
from flask import abort, request, jsonify, current_app
from pydantic import BaseModel, ValidationError
from spectree import SecurityScheme, SpecTree
from spectree.models import Server
from neomodel import (
    RelationshipTo,
    RelationshipFrom, Relationship,
    RelationshipManager, RelationshipDefinition,
    UniqueIdProperty
)
from neomodel.exceptions import DoesNotExist


spec = SpecTree(
    "flask",
    title="National Police Data Collaborative Index",
    description=textwrap.dedent(
        """
        This API provides federated sharing of police data using a searchable
        index of police records. The index only contains information necessary
        for search and aggregation. NPDC partners contribute to the index while
        maintaining ownership over the full record. Partners can use the API to
        authorize users to access the full records on their systems. This thus
        facilitates federated access control and data ownership.
        """
    ),
    # The version of the API. 0.X.Y is initial development with breaking changes
    # allowed on minor version changes.
    version="0.1.0",
    # Version of the `/apidoc/openapi.json` format
    # https://swagger.io/specification/
    openapi_version="3.0.3",
    # Only document routes decorated with validators
    mode="strict",
    # By default, all routes require either cookie or bearer auth
    security={"cookieAuth": [], "bearerAuth": []},
    servers=[
        Server(
            url="",
            description="This Origin",
        ),
        Server(
            url="https://dev-api.nationalpolicedata.org",
            description="Development environment",
        ),
        Server(
            url="https://stage-api.nationalpolicedata.org",
            description="Staging environment",
        ),
        Server(
            url="https://api.nationalpolicedata.org",
            description="Production environment",
        ),
    ],
    security_schemes=[
        # Cookie auth is used by browsers for GET requests
        SecurityScheme(
            name="cookieAuth",
            data={
                "type": "apiKey",
                "name": "access_token_cookie",
                "in": "cookie",
            },
        ),
        # Bearer auth is used by other API consumers
        SecurityScheme(
            name="bearerAuth",
            data={
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            },
        ),
    ],
)


T = TypeVar("T", bound="JsonSerializable")


# Function that replaces jsonify to properly handle OrderedDicts
def ordered_jsonify(*args, **kwargs):
    """
    Return a JSON response with OrderedDict objects properly serialized,
    preserving their order. Behaves like Flask's jsonify.

    Args:
        *args: The arguments to pass to the function.
        **kwargs: The keyword arguments to pass to the function.

    Returns:
        Response: A Flask Response object with the JSON data.
    """
    # Determine the indentation and separators based on the app configuration
    indent = None
    separators = (',', ':')
    if current_app.config.get('JSONIFY_PRETTYPRINT_REGULAR', False):
        indent = 2
        separators = (', ', ': ')

    # Handle the arguments similar to how Flask's jsonify does
    if args and kwargs:
        raise TypeError('ordered_jsonify() behavior undefined when passed both args and kwargs')
    elif len(args) == 1:
        data = args[0]
    else:
        # For multiple arguments, create a list; for kwargs, create a dict
        data = args if args else kwargs

    # Serialize the data to JSON, ensuring that OrderedDicts preserve order
    json_str = json.dumps(
        data,
        indent=indent,
        separators=separators,
    )

    # Create and return the response
    return current_app.response_class(
        json_str,
        mimetype=current_app.config.get('JSONIFY_MIMETYPE', 'application/json')
    )


# A decorator to validate request bodies using Pydantic models
def validate_request(model: BaseModel):
    """
    Validate the request body using a Pydantic model.

    Args:
        model (BaseModel): The Pydantic model to use for validation.

    Returns:
        function: A decorator function that validates the request body.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                body = model(**request.json)
            except ValidationError as e:
                return jsonify({
                    "status": "Unprocessable Entity",
                    "message": "Invalid request body",
                    "errors": e.errors(),
                }), 422

            request.validated_body = body
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def paginate_results(
        data: list[JsonSerializable],
        page: int, per_page: int, max_per_page: int = 100):
    """
    Paginate a list of data and return a reponse dict. Items in the list must
    implement the JsonSerializable interface.

    Args:
        data (list): The list of data to paginate.
        page (int): The page number to return.
        per_page (int): The number of items per page.
        max_per_page (int): The maximum number of items per page.

    Returns:
        dict: The paginated data.
            results (list): The list of paginated data.
            page (int): The current page number.
            per_page (int): The number of items per page.
            total (int): The total number of items.
    """
    if per_page > max_per_page:
        per_page = max_per_page
    start = (page - 1) * per_page
    end = start + per_page
    results = data[start:end]
    return {
        "results": [item.to_dict() for item in results],
        "page": page,
        "per_page": per_page,
        "total": len(data),
    }


# Update Enums to work well with NeoModel
class PropertyEnum(Enum):
    """Use this Enum to convert the options to a dictionary."""
    @classmethod
    def choices(cls):
        return {item.value: item.name for item in cls}


# Makes a StructuredNode convertible to and from JSON and Dicts
class JsonSerializable:
    """Mix me into a database model to make it JSON serializable."""
    __hidden_properties__ = []
    __property_order__ = []

    def to_dict(self, include_relationships=True,
                exclude_fields=None):
        """
        Convert the node instance into a dictionary.
        Args:
            include_relationships (bool): Whether to include
            relationships in the output.

            exclude_fields (list): List of fields to exclude
            from serialization.

            field_order (list): List of fields to order the
            output by.

        Returns:
            dict: A dictionary representation of the node.
        """
        exclude_fields = exclude_fields or []
        field_order = self.__property_order__

        all_excludes = set(
            self.__hidden_properties__).union(set(exclude_fields))

        all_props = self.defined_properties()
        node_props = OrderedDict()

        if field_order:
            ordered_props = [prop for prop in field_order if prop in all_props]
        else:
            ordered_props = list(all_props.keys())

        # Serialize node properties
        for prop_name in ordered_props:
            if prop_name not in all_excludes:
                value = getattr(self, prop_name, None)
                node_props[prop_name] = value

        # Optionally add related nodes
        if include_relationships:
            relationships = {
                key: value for key, value in self.__class__.__dict__.items()
                if isinstance(value, RelationshipDefinition)
            }
            for key in relationships:
                if key in all_excludes:
                    continue
                rel_manager = getattr(self, key, None)
                if isinstance(rel_manager, RelationshipManager):
                    related_nodes = rel_manager.all()
                    node_props[key] = [
                        node.to_dict(include_relationships=False)
                        for node in related_nodes
                    ]
        return node_props

    def to_json(self):
        """Convert the node instance into a JSON string."""
        return ordered_jsonify(self.to_dict())

    @classmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        """
        Creates or updates an instance of the model from a dictionary.

        Args:
            data (dict): A dictionary containing data for the model instance.

        Returns:
            Instance of the model.
        """
        instance = None
        all_props = cls.defined_properties()

        # Handle unique properties to find existing instances
        unique_properties = {
            name: prop for name, prop in all_props.items()
            if getattr(
                prop, 'unique_index', False) or isinstance(
                    prop, UniqueIdProperty)
        }
        unique_props = {
            prop_name: data.get(prop_name)
            for prop_name in unique_properties
            if prop_name in data and data.get(prop_name) is not None
        }

        if unique_props:
            try:
                instance = cls.nodes.get(**unique_props)
                # Update existing instance
                for key, value in data.items():
                    if key in all_props:
                        setattr(instance, key, value)
            except DoesNotExist:
                # No existing instance, create a new one
                instance = cls(**unique_props)
        else:
            instance = cls()

        # Set properties
        for key, value in data.items():
            if key in all_props:
                setattr(instance, key, value)

        # Handle relationships if they exist in the dictionary
        for key, value in data.items():
            if key.endswith("_uid"):
                rel_name = key[:-4]

                # See if a relationship manager exists for the pair
                if isinstance(
                    getattr(cls, rel_name, None), RelationshipManager
                ):
                    rel_manager = getattr(instance, rel_name)

                    # Fetch the related node by its unique identifier
                    related_node_class = rel_manager.definition['node_class']
                    try:
                        related_instance = related_node_class.nodes.get(
                            uid=value)
                        rel_manager.connect(related_instance)
                    except DoesNotExist:
                        raise ValueError(f"Related {related_node_class.__name__} with UID {value} not found.")
            # Handle relationship properties
            if key.endswith("_details"):
                rel_name = key[:-8]
                if isinstance(getattr(cls, rel_name, None), RelationshipManager):
                    rel_manager = getattr(instance, rel_name)
                    if rel_manager.exists():
                        relationship = rel_manager.relationship(
                            related_instance)
                        setattr(relationship, key, value)
                        relationship.save()
        # Save the instance
        instance.save()
        return instance

    @classmethod
    def __all_properties__(cls) -> List[str]:
        """Get a list of all properties defined in the class."""
        return [prop_name for prop_name in cls.__dict__ if isinstance(
            cls.__dict__[prop_name], property)]

    @classmethod
    def __all_relationships__(cls) -> dict:
        """Get all relationships defined in the class."""
        return {
            rel_name: rel_manager for rel_name, rel_manager in cls.__dict__.items()
            if isinstance(
                rel_manager, (RelationshipTo, RelationshipFrom, Relationship))
        }

    @classmethod
    def get(cls: Type[T], uid: Any, abort_if_null: bool = True) -> Optional[T]:
        """
        Get a model instance by its UID, returning None if
        not found (or aborting).

        Args:
            uid: Unique identifier for the node (could be Neo4j internal ID
             or custom UUID).
            abort_if_null (bool): Whether to abort if the node is not found.

        Returns:
            Optional[T]: An instance of the model or None.
        """
        obj = cls.nodes.get_or_none(uid=uid)
        if obj is None and abort_if_null:
            abort(404)
        return obj  # type: ignore
