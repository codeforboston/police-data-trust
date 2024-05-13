# flake8:noqa
"""adding officer search

Revision ID: 8ed5de17d4e6
Revises: cb88392372ed
Create Date: 2024-05-10 22:48:40.199373

"""
from alembic import op
import sqlalchemy as sa
# import backend.database.models.types
from backend.database.models import officer


# revision identifiers, used by Alembic.
revision = '8ed5de17d4e6'
down_revision = 'cb88392372ed'
branch_labels = None
depends_on = None

TRIGGER_TUPLES = [('stateID', 'state')]

index_set = [
    "tsv_stateID_state"
]


def upgrade():
    # grab a connection to the database
    conn = op.get_bind()
    # create the materialized view
    conn.execute(sa.sql.text('''
        CREATE MATERIALIZED VIEW officer_view AS
            SELECT
                ROW_NUMBER() OVER () AS id,
                officer.first_name AS officer_first_name,
                officer.middle_name AS officer_middle_name,
                officer.last_name AS officer_last_name,
                officer.date_of_birth AS officer_date_of_birth,
                "stateID".state AS "stateID_state",
                to_tsvector("stateID".state::text) AS "tsv_stateID_state",
                "stateID".value AS "stateID_value"
            FROM officer
            JOIN "stateID" ON officer.id = "stateID".officer_id;
    '''))
    # create unique index on ids
    op.create_index(op.f('idx_officer_view_id'),
                    'officer_view',
                    ['id'],
                    unique=True)

    # create remaining indices on the tsv columns
    for index in index_set:
        op.create_index(op.f(
            'idx_tsv_{}'.format(index)),
            'officer_view', [index],
            postgresql_using='gin'
        )

    # refresh materialzied view trigger
    conn.execute(sa.sql.text('''
        CREATE OR REPLACE FUNCTION trig_refresh_officer_view() RETURNS trigger AS
        $$
        BEGIN
            REFRESH MATERIALIZED VIEW CONCURRENTLY officer_view;
            RETURN NULL;
        END;
        $$
        LANGUAGE plpgsql ;
    '''))
    for table, column in TRIGGER_TUPLES:
        conn.execute(sa.sql.text('''
            DROP TRIGGER IF EXISTS "tsv_{table}_{column}_trigger" ON "{table}"
        '''.format(table=table, column=column)))
        conn.execute(sa.sql.text('''
            CREATE TRIGGER "tsv_{table}_{column}_trigger" AFTER
            TRUNCATE OR INSERT OR DELETE OR UPDATE OF "{column}"
            ON "{table}" FOR EACH STATEMENT
            EXECUTE PROCEDURE trig_refresh_officer_view()
        '''.format(table=table, column=column)))


def downgrade():
    # grab a connection to the database
    conn = op.get_bind()
    # drop the materialized view
    conn.execute(sa.sql.text('''
        DROP MATERIALIZED VIEW officer_view
    '''))
    for table, column in TRIGGER_TUPLES:
        conn.execute(sa.sql.text('''
            DROP TRIGGER IF EXISTS "tsv_{table}_{column}_trigger" ON "{table}"
        '''.format(table=table, column=column)))