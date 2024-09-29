import json
from typing import Any, Optional, TypeVar, Type, List
from collections import OrderedDict
from enum import Enum
from flask import abort, jsonify
from neomodel import (
    RelationshipTo,
    RelationshipFrom, Relationship,
    RelationshipManager, RelationshipDefinition
)
from neomodel.exceptions import DoesNotExist


T = TypeVar("T", bound="JsonSerializable")


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
        return jsonify(self.to_dict())

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
        unique_props = {
            prop: data.get(prop)
            for prop in all_props if prop in data
        }

        if unique_props:
            try:
                instance = cls.nodes.get(**unique_props)
                # Update existing instance
                for key, value in data.items():
                    if key in instance.__all_properties__:
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
                        relationship = rel_manager.relationship(related_instance)
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
