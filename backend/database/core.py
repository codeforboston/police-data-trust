"""This file defines the database connection, plus some terminal commands for
setting up and tearing down the database.

Do not import anything directly from `backend.database._core`. Instead, import
from `backend.database`.
"""
import os
from typing import Any, Optional

import click
import pandas as pd
import psycopg
import psycopg2.errors
from flask import abort, current_app
from flask.cli import AppGroup, with_appcontext
from flask_sqlalchemy import SQLAlchemy
from psycopg2 import connect
from psycopg2.extensions import connection
from sqlalchemy.exc import ResourceClosedError
from werkzeug.utils import secure_filename

from ..config import TestingConfig
from ..utils import dev_only
from typing import TypeVar, Type

db = SQLAlchemy()

T = TypeVar("T")


class CrudMixin:
    """Mix me into a database model whose CRUD operations you want to expose in
    a convenient manner.
    """

    def create(self: T, refresh: bool = True) -> T:
        db.session.add(self)
        db.session.commit()
        if refresh:
            db.session.refresh(self)
        return self

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(cls: Type[T], id: Any, abort_if_null: bool = True) -> Optional[T]:
        obj = db.session.query(cls).get(id)
        if obj is None and abort_if_null:
            abort(404)
        return obj  # type: ignore


QUERIES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "queries")
)


def execute_query(filename: str) -> Optional[pd.DataFrame]:
    """Run SQL from a file. It will return a Pandas DataFrame if it selected
    anything; otherwise it will return None.

    I do not recommend you use this function too often. In general we should be
    using the SQLAlchemy ORM. That said, it's a nice convenience, and there are
    times where this function is genuinely something you want to run.
    """
    with open(os.path.join(QUERIES_DIR, secure_filename(filename))) as f:
        query = f.read()
    with db.engine.connect() as conn:
        res = conn.execute(query)
        try:
            df = pd.DataFrame(res.fetchall(), columns=res.keys())
            return df
        except ResourceClosedError:
            return None


@click.group("psql", cls=AppGroup)
@with_appcontext
@click.pass_context
def db_cli(ctx: click.Context):
    """Collection of database commands."""
    conn = connect(
        user=current_app.config["POSTGRES_USER"],
        password=current_app.config["POSTGRES_PASSWORD"],
        host=current_app.config["POSTGRES_HOST"],
        port=current_app.config["POSTGRES_PORT"],
        dbname="postgres",
    )
    conn.autocommit = True
    ctx.obj = conn


pass_psql_admin_connection = click.make_pass_decorator(connection)


@db_cli.command("create")
@click.option(
    "--overwrite/--no-overwrite",
    default=False,
    is_flag=True,
    show_default=True,
    help="If true, overwrite the database if it exists.",
)
@pass_psql_admin_connection
@click.pass_context
@dev_only
def create_database(
    ctx: click.Context, conn: connection, overwrite: bool = False
):
    """Create the database from nothing."""
    database = current_app.config["POSTGRES_DB"]
    cursor = conn.cursor()

    if overwrite:
        cursor.execute(
            f"SELECT bool_or(datname = '{database}') FROM pg_database;"
        )
        exists = cursor.fetchall()[0][0]
        if exists:
            ctx.invoke(delete_database)

    try:
        cursor.execute(f"CREATE DATABASE {database};")
    except (psycopg2.errors.lookup("42P04"), psycopg.errors.DuplicateDatabase):
        click.echo(f"Database {database!r} already exists.")
    else:
        click.echo(f"Created database {database!r}.")


@db_cli.command("init")
def init_database():
    """Initialize the database schemas.

    Run this after the database has been created.
    """
    database = current_app.config["POSTGRES_DB"]
    db.create_all()
    click.echo(f"Initialized the database {database!r}.")


@db_cli.command("gen-examples")
def gen_examples_command():
    """Generate 2 incident examples in the database."""
    execute_query("example_incidents.sql")
    click.echo("Added 2 example incidents to the database.")


@db_cli.command("delete")
@click.option(
    "--test-db",
    "-t",
    default=False,
    is_flag=True,
    help=f"Deletes the database {TestingConfig.POSTGRES_DB!r}.",
)
@pass_psql_admin_connection
@dev_only
def delete_database(conn: connection, test_db: bool):
    """Delete the database."""
    if test_db:
        database = TestingConfig.POSTGRES_DB
    else:
        database = current_app.config["POSTGRES_DB"]

    cursor = conn.cursor()

    # Don't validate name for `police_data_test`.
    if database != TestingConfig.POSTGRES_DB:
        # Make sure we want to do this.
        click.echo(f"Are you sure you want to delete database {database!r}?")
        click.echo(
            "Type in the database name '"
            + click.style(database, fg="red")
            + "' to confirm"
        )
        confirmation = click.prompt("Database name")
        if database != confirmation:
            click.echo(
                "The input does not match. " "The database will not be deleted."
            )
            return None

    try:
        cursor.execute(f"DROP DATABASE {database};")
    except psycopg2.errors.lookup("3D000"):
        click.echo(f"Database {database!r} does not exist.")
    else:
        click.echo(f"Database {database!r} was deleted.")
