"""This file defines the database connection, plus some terminal commands for
setting up and tearing down the database.

Do not import anything directly from `backend.database._core`. Instead, import
from `backend.database`.
"""
import os
from typing import Optional

import click
import pandas as pd
from flask import current_app
from flask.cli import AppGroup, with_appcontext
from werkzeug.utils import secure_filename
from neomodel import install_all_labels
from neo4j import Driver

from ..utils import dev_only


QUERIES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "queries")
)


def execute_query(filename: str) -> Optional[pd.DataFrame]:
    """Run a Cypher query from a file using the provided Neo4j connection.

    It returns a Pandas DataFrame if the query yields results; otherwise,
    it returns None.
    """
    # Read the query from the file
    query_path = os.path.join(QUERIES_DIR, secure_filename(filename))
    with open(query_path, 'r') as f:
        query = f.read()

    # Get the Neo4j driver
    neo4j_conn = current_app.config['DB_DRIVER']

    # Execute the query using the existing connection
    with neo4j_conn.session() as session:
        result = session.run(query)
        records = list(result)

        if records:
            # Convert Neo4j records to a list of dictionaries
            data = [record.data() for record in records]
            # Create a DataFrame
            df = pd.DataFrame(data)
            return df
        else:
            return None


@click.group("neo4j", cls=AppGroup)
@with_appcontext
@click.pass_context
def db_cli():
    """Collection of Neo4j database commands."""
    pass


# Decorator to pass the Neo4j driver
pass_neo4j_driver = click.make_pass_decorator(Driver)


@db_cli.command("create")
@click.option(
    "--overwrite/--no-overwrite",
    default=False,
    is_flag=True,
    show_default=True,
    help="If true, overwrite the database by deleting existing data.",
)
@with_appcontext
@dev_only
def create_database(overwrite: bool):
    """Initialize the Neo4j database by setting up constraints and indexes."""
    if overwrite:
        # Get the Neo4j driver
        neo4j_conn = current_app.config['DB_DRIVER']

        with neo4j_conn.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        click.echo("Existing data deleted from the database.")

    # Install constraints and indexes for all models
    install_all_labels()

    click.echo("Initialized the Neo4j database with constraints and indexes.")


@db_cli.command("init")
@with_appcontext
def init_database():
    """Initialize the Neo4j database by setting up constraints and indexes."""

    # Install constraints and indexes
    install_all_labels()
    click.echo("Initialized the Neo4j database with constraints and indexes.")


@db_cli.command("gen-examples")
@pass_neo4j_driver
def gen_examples_command():
    """Generate example data in the Neo4j database."""
    # Use your existing execute_query function
    execute_query("example_data.cypher")
    click.echo("Added example data to the Neo4j database.")


@db_cli.command("delete")
@click.option(
    "--test-db",
    "-t",
    default=False,
    is_flag=True,
    help="Deletes the test database.",
)
@with_appcontext
@dev_only
def delete_database(test_db: bool):
    """Delete all data from the Neo4j database."""
    if test_db:
        # If you have a separate test database, drop it
        test_neo4j_conn = current_app.config['DB_DRIVER']
        test_db_name = current_app.config.get("GRAPH_TEST_DB_NAME", "test")
        with test_neo4j_conn.session(database="system") as session:
            session.run(f"DROP DATABASE {test_db_name} IF EXISTS")
        click.echo(f"Test database {test_db_name!r} was deleted.")
    else:
        # Delete all data from the default database
        neo4j_conn = current_app.config['DB_DRIVER']
        with neo4j_conn.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        click.echo("Deleted all data from the Neo4j database.")
