import json
from enum import Enum
from neomodel import (
    StructuredNode, RelationshipTo,
    RelationshipFrom, Relationship
)
from neomodel.exceptions import DoesNotExist


class PropertyEnum(Enum):

    @classmethod
    def choices(cls):
        return {item.value: item.name for item in cls}


class ExportableNode(StructuredNode):
    def to_dict(self):
        # Collect all properties dynamically
        node_props = {
            prop_name: getattr(self, prop_name) for prop_name in self.__all_properties__()
        }

        # Handle ID separately if needed
        node_props['id'] = self.id

        # Optionally add related nodes, if needed
        for rel_name, rel_manager in self.__all_relationships__().items():
            related_nodes = rel_manager.all()
            node_props[rel_name] = [node.to_dict() for node in related_nodes]

        return node_props

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data):
        """
        Creates or updates an instance of the model from a dictionary.
        
        Args:
            data (dict): A dictionary containing data for the model instance.
        
        Returns:
            Instance of the model.
        """
        instance = None

        # Handle unique properties to find existing instances
        unique_props = {prop: data.get(prop) for prop in cls.__all_properties__() if prop in data}

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

        # Handle relationships (assuming relationships are also in the dictionary)
        for rel_name, rel_manager in cls.__all_relationships__().items():
            if rel_name in data:
                related_nodes = data[rel_name]
                if isinstance(related_nodes, list):
                    # Assume related_nodes is a list of dictionaries
                    for rel_data in related_nodes:
                        related_instance = rel_manager.definition['node_class'].from_dict(rel_data)
                        getattr(instance, rel_name).connect(related_instance)
                else:
                    # Assume related_nodes is a single dictionary
                    related_instance = rel_manager.definition['node_class'].from_dict(related_nodes)
                    getattr(instance, rel_name).connect(related_instance)

        instance.save()
        return instance

    @classmethod
    def __all_properties__(cls):
        return [prop_name for prop_name in cls.__dict__ if isinstance(
            cls.__dict__[prop_name], property)]

    @classmethod
    def __all_relationships__(cls):
        return {
            rel_name: rel_manager for rel_name, rel_manager in cls.__dict__.items() if isinstance(
                rel_manager, (RelationshipTo, RelationshipFrom, Relationship))}
