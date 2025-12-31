from __future__ import annotations
import math
import json
import datetime
import logging
import textwrap
from functools import wraps
from enum import Enum
from collections import OrderedDict
from typing import Any, Optional, TypeVar, Type, List, Dict, Tuple
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


# Returns a single page from a set of data
# Deprecated: Use `add_pagination_wrapper` instead
def paginate_results(
        data: list[JsonSerializable],
        page: int, per_page: int = 20, max_per_page: int = 100):
    """
    Deprecated: Use `add_pagination_wrapper` instead.
    Paginate a list of data and return a reponse dict that includes a single
    page of results. Items in the list must implement the JsonSerializable
    interface.

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


# Add pagination to a list of data and return a response dict.
def add_pagination_wrapper(
        page_data: list, total: int,
        page_number: int = 1, per_page: int = 20):
    """
    Add the paginated response properties to a preselected page of results.
    Args:
        page_data (list): The list of data to paginate.
        page_number (int): The page number to return.
        per_page (int): The number of items per page.
        max_per_page (int): The maximum number of items per page.
    Returns:
        dict: The paginated data.
    """
    if len(page_data) == 0 and total == 0:
        return {
            "results": [],
            "page": 1,
            "per_page": per_page,
            "total": 0,
            "pages": 0
        }
    expected_total_pages = math.ceil(total / per_page)
    if not page_number <= expected_total_pages:
        abort(400, description="Page number exceeds total results")
    return {
        "results": page_data,
        "page": page_number,
        "per_page": per_page,
        "total": total,
        "pages": expected_total_pages
    }


def args_to_dict(args, always_list=frozenset()) -> dict:
    """
    Convert a Flask request.args MultiDict to a regular dictionary.
    Args:
        args (MultiDict): The Flask request.args MultiDict.
    Returns:
        dict: A regular dictionary with the same keys and values.
    """
    raw = args.to_dict(flat=False)
    data = {}
    for k, v in raw.items():
        if k in always_list:
            data[k] = v
        else:
            data[k] = v[0] if len(v) == 1 else v
    return data


# A tiny, read-only, chainable relation view.
class RelQuery:
    """
    A tiny, read-only, chainable relation view.
    Usage:
        agency.units.filter(
           "u.name CONTAINS $q", q="SWAT").order_by("u.name").limit(5).all()
        agency.units.first()
        agency.units.exists()
        agency.units.one()  # raises if != 1
    """
    def __init__(
            self, owner: StructuredNode, base_cypher: str,
            return_alias: str, inflate_cls, distinct: bool = False):
        self._owner = owner
        self._base = base_cypher.strip().rstrip(";")
        self._ret = return_alias
        self._inflate = inflate_cls
        self._where: List[str] = []
        self._params: Dict[str, Any] = {"uid": owner.uid}
        self._distinct = distinct
        self._order: Optional[str] = None
        self._limit: Optional[int] = None

    # ---- builders ----
    def filter(self, clause: str, /, **params):
        if clause:
            self._where.append(f"({clause})")
        if params:
            self._params.update(params)
        return self

    def params(self, **params):
        self._params.update(params)
        return self

    def order_by(self, clause: str):
        self._order = clause
        return self

    def limit(self, n: int):
        self._limit = n
        return self

    # ---- executors ----
    def _compose(self, count_only: bool = False) -> Tuple[str, Dict[str, Any]]:
        parts = [self._base]
        if self._where:
            parts.append("WHERE " + " AND ".join(self._where))
        if count_only:
            parts.append(f"RETURN count({self._ret}) AS c")
        else:
            if self._distinct:
                parts.append(f"RETURN DISTINCT {self._ret} AS node")
            else:
                parts.append(f"RETURN {self._ret} AS node")
            if self._order:
                parts.append(f"ORDER BY {self._order}")
            if self._limit is not None:
                parts.append(f"LIMIT {self._limit}")
        return " ".join(parts) + ";", self._params

    def all(self):
        cy, params = self._compose()
        rows, _ = db.cypher_query(cy, params, resolve_objects=True)
        # if resolve_objects=True is wired, rows come back as objects already
        if rows and not isinstance(rows[0][0], StructuredNode):
            # fallback inflate (in case resolve_objects isn't used)
            return [self._inflate.inflate(row[0]) for row in rows]
        return [row[0] for row in rows]

    def first(self):
        if self._limit is None:
            self.limit(1)
        res = self.all()
        return res[0] if res else None

    def one(self):
        # exactly one or raise
        res = self.limit(2).all()
        if len(res) != 1:
            raise ValueError(f"Expected exactly one result, got {len(res)}")
        return res[0]

    def exists(self) -> bool:
        cy, params = self._compose(count_only=True)
        rows, _ = db.cypher_query(cy, params)
        return bool(rows and rows[0][0] > 0)

    def count(self) -> int:
        """
        Count the number of nodes matching the query.
        Returns:
            int: The count of nodes.
        """
        cy, params = self._compose(count_only=True)
        rows, _ = db.cypher_query(cy, params)
        return rows[0][0] if rows else 0


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
    __virtual_relationships__ = []

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
        # Add virtual relationships
        for rel_name in self.__virtual_relationships__:
            if rel_name in all_excludes:
                continue
            rel_query = getattr(self, rel_name, None)
            if isinstance(rel_query, RelQuery):
                related_nodes = rel_query.limit(relationship_limit).all()
                obj_props[rel_name] = [
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


class SearchableMixin:
    """
    Base mixin for any model that wants a searchable interface.
    """

    @classmethod
    def _preprocess_query(cls, query: str, watchlist) -> str:
        """
        Preprocess the search query before using it in fulltext search.
        Args:
            query (str): The original search query.
        Returns:
            str: The preprocessed search query.
        """
        query_terms = query.split()
        processed_terms = []
        for term in query_terms:
            if term.lower() in watchlist:
                continue  # skip common terms
            processed_terms.append(term)
        query = " ".join(processed_terms)
        return query

    @classmethod
    def _search(
        cls,
        label: str,
        index: str | None = None,
        filters: dict | None = None,
        query: str | None = None,
        count: bool = False,
        skip: int = 0,
        limit: int = 25,
        extra_params: dict | None = None,
    ):
        """
        Generic search executor for any node label.

        Args:
            label: Neo4j node label
            index: Optional fulltext index Cypher snippet (from search)
            filters: Dict of field->value for exact matches
            query: Optional fulltext search term
            count: Return count instead of nodes
            skip: Pagination offset
            limit: Pagination limit
            extra_params: Additional parameters to pass to the Cypher query

        Returns:
            int if count=True, else list of nodes
        """
        filters = filters or {}
        params = filters.copy()
        if extra_params:
            params.update(extra_params)

        cypher_parts = []

        # Use fulltext index if provided
        if index:
            cypher_parts.append(index)

        cypher_parts.append(f"MATCH (n:{label})")

        # Property filters
        if filters:
            where_clause = " AND ".join(f"n.{k} = ${k}" for k in filters)
            if any("WHERE" in part for part in cypher_parts):
                # Append to existing WHERE from fulltext
                cypher_parts.append("AND " + where_clause)
            else:
                cypher_parts.append("WHERE " + where_clause)

        # Return count or nodes
        if count:
            cypher_parts.append("RETURN count(n) AS count")
        else:
            cypher_parts.append("RETURN n SKIP $skip LIMIT $limit")
            params.update({"skip": skip, "limit": limit})

        cypher = "\n".join(cypher_parts)

        logging.warning(f"Search Cypher:\n{cypher}\nWith params: {params}")
        rows, _ = db.cypher_query(cypher, params)

        if count:
            return rows[0][0] if rows else 0
        return [row[0] for row in rows]
