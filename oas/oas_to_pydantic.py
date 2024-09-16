#!/usr/bin/env python3

import argparse
import yaml
import os
import sys


class OASModelGenerator:
    def __init__(self, oas, verbose=False):
        self.oas = oas
        self.verbose = verbose

    def parse_property(self, prop_name, prop_details):
        """Parse a single property from the schema to
        generate a Pydantic field."""
        pydantic_type_map = {
            "string": "str",
            "number": "float",
            "integer": "int",
            "boolean": "bool",
            "array": "List",
            "object": "Dict"
        }

        if 'type' in prop_details:
            prop_type = pydantic_type_map.get(prop_details['type'], "Any")
            if prop_details['type'] == "array":
                items_type, _ = self.parse_property(None, prop_details['items'])
                return f"List[{items_type}]", prop_details.get('description')
            elif prop_details['type'] == "object":
                if 'properties' in prop_details:
                    # For nested objects, we'll use
                    # Dict[str, Any] for simplicity.
                    return "Dict[str, Any]", prop_details.get('description')
                else:
                    return "Dict[str, Any]", prop_details.get('description')
            else:
                return prop_type, prop_details.get('description')
        elif '$ref' in prop_details:
            # Handle references
            ref = prop_details['$ref'].split('/')[-1]
            return ref, prop_details.get('description')
        elif 'oneOf' in prop_details:
            # Handle oneOf by creating a Union type
            union_types = [
                ref.split('/')[-1] if '$ref' in ref else "Any"
                for ref in prop_details['oneOf']
            ]
            union_str = "Union[" + ", ".join(union_types) + "]"
            return union_str, prop_details.get('description')
        elif 'allOf' in prop_details:
            # Handle allOf by combining referenced schemas
            combined_type = None
            description = prop_details.get('description')

            # Process each part of allOf
            for item in prop_details['allOf']:
                if '$ref' in item:
                    ref = item['$ref'].split('/')[-1]
                    combined_type = ref
                elif 'type' in item and not combined_type:
                    prop_type = pydantic_type_map.get(item['type'], "Any")
                    combined_type = prop_type

                if 'description' in item:
                    description = item['description']
            return combined_type, description
        else:
            return "Any", prop_details.get('description')

    def process_all_of(self, schema_details):
        """Process 'allOf' by merging properties and handling inheritance.
        """
        combined_properties = {}
        required_props = set()
        parent_classes = []

        for item in schema_details['allOf']:
            if '$ref' in item:
                # Handle refrence in 'allOf'
                ref = item['$ref'].split('/')[-1]
                ref_schema = self.oas.get(
                    'components', {}).get('schemas', {}).get(ref, {})
                if ref_schema:
                    # Parent class found
                    # Merge properties from the refernced schema
                    ref_properties = ref_schema.get('properties', {})
                    combined_properties.update(ref_properties)

                    # Merge required properties
                    required_props.update(ref_schema.get('required', []))
                    parent_classes.append(ref)
                else:
                    # Parent schema not found (likely in an external file)
                    # Keep the parent class name for inheritance but
                    # treat the child as defining the model
                    parent_classes.append(ref)

            elif 'properties' in item:
                # If additional properties are defined within the 'allOf'
                additional_properties = item.get('properties', {})
                combined_properties.update(additional_properties)
                required_props.update(item.get('required', []))

        return combined_properties, required_props, parent_classes

    def generate_pydantic_model(self, schema_name, schema_details, indent=4):
        """Generate a Pydantic model for a given schema."""
        class_def = f"class {schema_name}(BaseModel):\n"
        if self.verbose:
            print(f"Generating model code for {schema_name}")

        if 'description' in schema_details:
            class_def += f'    """{schema_details["description"]}"""\n'

        if 'allOf' in schema_details:
            # Handle allOf (merging or inheritance)
            properties, required_props, parent_classes = self.process_all_of(
                schema_details)
            if parent_classes:
                # Add parent classes to inheritance
                class_def = "class {}({}, BaseModel):\n".format(
                    schema_name,
                    ', '.join(parent_classes)
                )
        else:
            # Handle regular properties if allOf is not present
            properties = schema_details.get('properties', {})
            required_props = schema_details.get('required', [])

        if not properties:
            class_def += "    pass\n"
            return class_def

        for prop_name, prop_details in properties.items():
            prop_type, prop_description = self.parse_property(
                prop_name, prop_details)

            # Determine if the property is required
            if prop_name in required_props:
                default = "..."
            else:
                default = "None"
                prop_type = f"Optional[{prop_type}]"

            field_str = f"{prop_name}: {prop_type}"
            if prop_description:
                field_str += " = Field({}, description=\"{}\")".format(
                    default,
                    prop_description,
                )
            else:
                field_str += f" = {default}"
            class_def += f"    {field_str}\n"

        return class_def

    def generate_models_from_oas(self):
        """Generate Pydantic models from the OAS components/schemas."""
        schemas = self.oas.get('components', {}).get('schemas', {})

        models = []
        for schema_name, schema_details in schemas.items():
            model_code = self.generate_pydantic_model(
                schema_name, schema_details)
            models.append(model_code)

        return models


def main():
    parser = argparse.ArgumentParser(
        description="Generate Pydantic models from an " +
        "OpenAPI Specification (OAS) YAML file."
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the OpenAPI YAML file."
    )
    parser.add_argument(
        "output_file",
        type=str,
        help="Path to the output Python file where" +
        "Pydantic models will be saved."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output."
    )

    args = parser.parse_args()

    input_path = args.input_file
    output_path = args.output_file
    verbose = args.verbose

    if not os.path.isfile(input_path):
        print(
            "Error: The input file '{}' does not exist.".format(
                input_path
            ), file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_path, 'r') as f:
            oas = yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading the input file: {e}", file=sys.stderr)
        sys.exit(1)

    if verbose:
        print(f"Loaded OpenAPI Specification from '{input_path}'.")

    generator = OASModelGenerator(oas, verbose)
    models = generator.generate_models_from_oas()

    if not models:
        print("No schemas found in the OpenAPI Specification.", file=sys.stderr)
        sys.exit(1)

    # Add necessary imports at the top of the output file
    import_statements = [
        "from pydantic import BaseModel, Field",
        "from typing import List, Optional, Dict, Any, Union",
        "",
        "",
    ]

    try:
        with open(output_path, 'w') as f:
            for line in import_statements:
                f.write(line + "\n")
            for model in models:
                f.write(model + "\n\n")
    except Exception as e:
        print(f"Error writing to the output file: {e}", file=sys.stderr)
        sys.exit(1)

    print(
        "Pydantic models have been successfully" +
        " generated and saved to '{}'.".format(
            output_path))


if __name__ == "__main__":
    main()
