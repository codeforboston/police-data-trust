"""agency location search

Revision ID: cb88392372ed
Revises:
Create Date: 2024-05-07 01:52:00.195324

"""
from alembic import op
import sqlalchemy as sa
# import backend.database.models.types


# revision identifiers, used by Alembic.
revision = 'cb88392372ed'
down_revision = None
branch_labels = None
depends_on = None

TRIGGER_TUPLES = [('agency', 'hq_address'),
                  ('agency', 'hq_city'),
                  ('agency', 'hq_zip'),
                  ]

index_set = [
    "tsv_agency_hq_address",
    "tsv_agency_hq_city",
    "tsv_agency_hq_zip",
]


def upgrade():
    # grab a connection to the database
    conn = op.get_bind()
    # create the materialized view
    conn.execute(sa.sql.text('''
        CREATE MATERIALIZED VIEW agency_view AS
            (SELECT
                id AS agency_id,
                name AS agency_name,
                website_url AS agency_website_url,
                hq_address AS agency_hq_address,
                to_tsvector(hq_address) AS tsv_agency_hq_address,
                hq_city AS agency_hq_city,
                to_tsvector(hq_city) AS tsv_agency_hq_city,
                hq_zip AS agency_hq_zip,
                to_tsvector(hq_zip) AS tsv_agency_hq_zip,
                jurisdiction AS agency_jurisdiction
                FROM agency
        )
    '''))
    # create unique index on ids
    op.create_index(op.f('idx_agency_view_id'),
                    'agency_view',
                    ['agency_id'],
                    unique=True)

    # create remaining indices on the tsv columns
    for index in index_set:
        op.create_index(op.f(
            'idx_tsv_{}'.format(index)),
            'agency_view', [index],
            postgresql_using='gin'
        )

    # refresh materialzied view trigger
    conn.execute(sa.sql.text('''
        CREATE OR REPLACE FUNCTION trig_refresh_agency_view() RETURNS trigger AS
        $$
        BEGIN
            REFRESH MATERIALIZED VIEW CONCURRENTLY agency_view;
            RETURN NULL;
        END;
        $$
        LANGUAGE plpgsql ;
    '''))
    for table, column in TRIGGER_TUPLES:
        conn.execute(sa.sql.text('''
            DROP TRIGGER IF EXISTS tsv_{table}_{column}_trigger ON {table}
        '''.format(table=table, column=column)))
        conn.execute(sa.sql.text('''
            CREATE TRIGGER tsv_{table}_{column}_trigger AFTER
            TRUNCATE OR INSERT OR DELETE OR UPDATE OF {column}
            ON {table} FOR EACH STATEMENT
            EXECUTE PROCEDURE trig_refresh_agency_view()
        '''.format(table=table, column=column)))


def downgrade():
    # grab a connection to the database
    conn = op.get_bind()
    # drop the materialized view
    conn.execute(sa.sql.text('''
        DROP MATERIALIZED VIEW agency_view
    '''))
    for table, column in TRIGGER_TUPLES:
        conn.execute(sa.sql.text('''
            DROP TRIGGER IF EXISTS tsv_{table}_{column}_trigger ON {table}
        '''.format(table=table, column=column)))
