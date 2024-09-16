"""This file defines the database connection, plus some terminal commands for
setting up and tearing down the database.

Do not import anything directly from `backend.database._core`. Instead, import
from `backend.database`.
"""
import os
import json
from typing import Any, Optional, TypeVar, Type, List
from enum import Enum

import click
import pandas as pd
from flask import abort, current_app
from flask.cli import AppGroup, with_appcontext
from werkzeug.utils import secure_filename
from neomodel import (
    db, RelationshipTo,
    RelationshipFrom, Relationship
)
from neo4j import GraphDatabase
from neomodel.exceptions import DoesNotExist

from ..config import TestingConfig
from ..utils import dev_only


T = TypeVar("T", bound="JsonSerializable")


class JsonSerializable:
    """Mix me into a database model to make it JSON serializable."""

    def to_dict(self, include_relationships=True):
        """
        Convert the node instance into a dictionary.
        Args:
            include_relationships (bool): Whether to include
            relationships in the output.
        
        Returns:
            dict: A dictionary representation of the node.
        """
        # Serialize node properties using deflate to handle conversions
        node_props = self.deflate(self.__properties__)

        # Optionally add related nodes
        if include_relationships:
            for rel_name, rel_manager in self.__all_relationships__().items():
                related_nodes = rel_manager.all()
                node_props[rel_name] = [
                    node.to_dict(include_relationships=False)
                    for node in related_nodes
                ]

        return node_props

    def to_json(self):
        """Convert the node instance into a JSON string."""
        return json.dumps(self.to_dict())

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

        # Handle unique properties to find existing instances
        unique_props = {
            prop: data.get(prop)
            for prop in cls.__all_properties__() if prop in data and data.get(
                prop)
        }

        if unique_props:
            try:
                instance = cls.nodes.get(**unique_props)
                # Update existing instance
                for key, value in data.items():
                    if key in instance.__all_properties__():
                        setattr(instance, key, value)
            except DoesNotExist:
                # No existing instance, create a new one
                instance = cls(**unique_props)
        else:
            instance = cls()

        # Set properties
        for key, value in data.items():
            if key in instance.__all_properties__():
                setattr(instance, key, value)

        # Handle relationships if they exist in the dictionary
        for rel_name, rel_manager in cls.__all_relationships__().items():
            if rel_name in data:
                related_nodes = data[rel_name]
                if isinstance(related_nodes, list):
                    # Assume related_nodes is a list of dictionaries
                    for rel_data in related_nodes:
                        related_instance = rel_manager.definition[
                            'node_class'].from_dict(rel_data)
                        getattr(instance, rel_name).connect(related_instance)
                else:
                    # Assume related_nodes is a single dictionary
                    related_instance = rel_manager.definition[
                        'node_class'].from_dict(related_nodes)
                    getattr(instance, rel_name).connect(related_instance)

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


# Update Enums to work well with NeoModel
class PropertyEnum(Enum):
    """Mix me into an Enum to convert the options to a dictionary."""
    @classmethod
    def choices(cls):
        return {item.value: item.name for item in cls}


QUERIES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "queries")
)


# Neo4j commands
@click.group("neo4j", cls=AppGroup)
@with_appcontext
@click.pass_context
def neo4j_cli(ctx: click.Context):
    """Collection of Neo4j database commands."""
    neo4j_conn = GraphDatabase.driver(
        current_app.config["GRAPH_NM_URI"],
        auth=(
            current_app.config["GRAPH_USER"],
            current_app.config["GRAPH_PASSWORD"],
        ),
    )
    ctx.obj = neo4j_conn


@neo4j_cli.command("create")
@with_appcontext
def neo4j_create():
    """Create the Neo4j database or ensure it is ready."""
    # Example logic to create a constraint or ensure the database is ready
    db.cypher_query("CREATE CONSTRAINT ON (n:Node) ASSERT n.uid IS UNIQUE;")
    click.echo("Neo4j database setup complete.")


@neo4j_cli.command("delete")
@with_appcontext
def neo4j_delete():
    """Delete all nodes and relationships in the Neo4j database."""
    db.cypher_query("MATCH (n) DETACH DELETE n")
    click.echo("Neo4j database cleared.")
