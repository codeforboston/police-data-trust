from __future__ import annotations
import math
import json
import datetime
import logging
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
    UniqueIdProperty, StructuredRel, StructuredNode,
    db
)
from neomodel.exceptions import DoesNotExist

from backend.database.models.infra.locations import (
    StateNode, CityNode
)


spec = SpecTree(
    "flask",
    title="National Police Data Collaborative Index",
    description=textwrap.dedent(
        """
        This API provides federated sharing of police data using a searchable
        index of police records. The index only contains information necessary
        for search and aggregation. NPDC sources contribute to the index while
        maintaining ownership over the full record. Sources can use the API to
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


class NodeConflictException(Exception):
    """Exception raised when a node already exists in the database."""
    pass


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
        raise TypeError(
            'ordered_jsonify() behavior undefined when' +
            'passed both args and kwargs')
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
        page: int, per_page: int = 20, max_per_page: int = 100):
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
    expected_total_pages = math.ceil(len(data) / per_page)
    if not page <= expected_total_pages:
        abort(404)
    start = (page - 1) * per_page
    end = start + per_page
    results = data[start:end]
    return {
        "results": [item.to_dict() for item in results],
        "page": page,
        "per_page": per_page,
        "total": len(data),
        "pages": expected_total_pages,
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
                relationship_limit: int = 20, exclude_fields=None):
        """
        Convert the node instance into a dictionary, including
        its relationships.

        Args:
            include_relationships (bool): Whether to include relationships in
            the output. exclude_fields (list): List of fields to exclude from
            serialization.

        Returns:
            dict: A dictionary representation of the node.
        """
        exclude_fields = exclude_fields or []
        field_order = getattr(self, '__property_order__', None)

        all_excludes = set(
            getattr(self, '__hidden_properties__', [])).union(
                set(exclude_fields))

        all_props = self.defined_properties(aliases=False, rels=False)
        obj_props = OrderedDict()

        if field_order:
            ordered_props = [prop for prop in field_order if prop in all_props]
        else:
            ordered_props = list(all_props.keys())

        # Serialize properties
        for prop_name in ordered_props:
            if prop_name not in all_excludes:
                value = getattr(self, prop_name, None)
                if isinstance(value, (datetime.datetime, datetime.date)):
                    value = value.isoformat()
                obj_props[prop_name] = value

        # Optionally add related nodes
        if include_relationships and isinstance(self, StructuredNode):
            relationships = {
                key: value for key, value in self.__class__.__dict__.items()
                if isinstance(value, RelationshipDefinition)
            }
            for key, relationship_def in relationships.items():
                if key in all_excludes:
                    continue

                rel_manager = getattr(self, key, None)
                if isinstance(rel_manager, RelationshipManager):
                    related_nodes = rel_manager.all()[0:relationship_limit]
                    # Limit the number of related nodes to serialize
                    if relationship_def.definition.get('model', None):
                        # If there is a relationship model, serialize it as well
                        obj_props[key] = [
                            {
                                'node': node.to_dict(
                                    include_relationships=False),
                                'relationship': rel_manager.relationship(
                                    node).to_dict() if isinstance(
                                        rel_manager.relationship(
                                            node), StructuredRel) else {}
                            }
                            for node in related_nodes
                        ]
                    else:
                        # No specific relationship model, just serialize nodes
                        obj_props[key] = [
                            node.to_dict(include_relationships=False)
                            for node in related_nodes
                        ]

        return obj_props

    def to_json(self):
        """Convert the node instance into a JSON string."""
        return ordered_jsonify(self.to_dict())

    @classmethod
    def from_dict(cls: Type[T], data: dict, uid=None) -> T:
        """
        Creates or updates an instance of the model from a dictionary.

        Args:
            data (dict): A dictionary containing data for the model instance.

        Returns:
            Instance of the model.
        """
        instance = None
        all_props = cls.defined_properties()
        if uid:
            # Find the instance by its UID
            instance = cls.nodes.get_or_none(uid=uid)
        else:
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
                    # If the instance exists, raise an error.
                    raise NodeConflictException(
                        "{} {} already exists".format(
                            cls.__name__,
                            instance.uid
                        ) + " with matching unique properties.")
                except DoesNotExist:
                    # No existing instance, create a new one
                    instance = cls(**unique_props)
            else:
                instance = cls()
        # Set properties
        for key, value in data.items():
            if key in all_props and value is not None:
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
                        raise ValueError(
                            "Related {} with UID {} not found.".format(
                                related_node_class.__name__,
                                value
                            ))
            # Handle relationship properties
            if key.endswith("_details"):
                rel_name = key[:-8]
                if isinstance(
                    getattr(cls, rel_name, None), RelationshipManager
                ):
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
    def __all_properties_JS__(cls) -> List[str]:
        """Get a list of all properties defined in the class."""
        return [prop_name for prop_name in cls.__dict__ if isinstance(
            cls.__dict__[prop_name], property)]

    @classmethod
    def __all_relationships_JS__(cls) -> dict:
        """Get all relationships defined in the class."""
        return {
            rel_name: rel_manager
            for rel_name, rel_manager in cls.__dict__.items()
            if isinstance(
                rel_manager,
                (RelationshipTo, RelationshipFrom, Relationship)
            )
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

    @classmethod
    def link_location(cls: Type[T], item, state=None, city=None):
        """
        Link a node to the relevant location nodes.

        :param item: The item to link
        :param state: The state. Should be a two-letter State code or name.
        :param county: The county. Should be a FIPS code or county name.
        :param city: The city. Should be a SimpleMaps ID or city name.
        """
        if state is not None:
            state_node = StateNode.nodes.get_or_none(
                abbreviation=state)
            if state_node:
                item.state_node.connect(state_node)
                logging.info(f"Linked {item.uid} to State {state_node.uid}")

                # Add city if provided
                if city is not None:
                    query = """
                    MATCH (c:CityNode
                    {name: $city})-[]-()-[]-(s:StateNode {uid: $state})
                    RETURN c LIMIT 25
                    """
                    results, meta = db.cypher_query(query, {
                        "city": city,
                        "state": state_node.uid
                    })
                    if results:
                        city_node = CityNode.inflate(results[0][0])
                        item.city_node.connect(city_node)
                        logging.info(
                            f"Linked {item.uid} to City {city_node.uid}")

            else:
                logging.error(f"State not found: {state}")
