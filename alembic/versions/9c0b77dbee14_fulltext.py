"""fulltext

Revision ID: 9c0b77dbee14
Revises: 
Create Date: 2024-04-21 02:53:30.947416

"""
from alembic import op
import sqlalchemy as sa
# import backend.database.models.types


# revision identifiers, used by Alembic.
revision = '9c0b77dbee14'
down_revision = None
branch_labels = None
depends_on = None
TRIGGER_TUPLES = [('officer', 'first_name'),
                  ('officer', 'last_name'),
                  ('officer', 'middle_name'),
                  ('agency', 'name')]

index_set = [
    "tsv_officer_first_name",
    "tsv_officer_last_name",
    "tsv_officer_middle_name",
    "tsv_agency_name",
]


def upgrade():
    # grab a connection to the database
    conn = op.get_bind()
    # create the materialized view
    conn.execute(sa.sql.text('''
        CREATE MATERIALIZED VIEW search_view AS
            (SELECT
                ROW_NUMBER() OVER () AS id,
                officer.id AS officer_id,
                officer.first_name              AS officer_first_name,
                to_tsvector(officer.first_name) AS tsv_officer_first_name,
                officer.middle_name             AS officer_middle_name,
                to_tsvector(officer.middle_name) AS tsv_officer_middle_name,
                officer.last_name               AS officer_last_name,
                to_tsvector(officer.last_name)  AS tsv_officer_last_name,
                officer.race AS officer_race,
                officer.ethnicity AS officer_ethnicity,
                officer.gender AS officer_gender,
                officer.date_of_birth AS officer_date_of_birth,
                agency.id AS agency_id,
                agency.name                     AS agency_name,
                to_tsvector(agency.name)        AS tsv_agency_name,
                agency.website_url AS agency_website_url,
                agency.hq_address AS agency_hq_address,
                agency.hq_city AS agency_hq_city,
                agency.hq_zip AS agency_hq_zip,
                agency.jurisdiction agency_jurisdiction
            FROM officer
            FULL OUTER JOIN agency ON
            officer.first_name = agency.name
        )
    '''))
    # create unique index on ids
    op.create_index(op.f('idx_search_view_id'),
                    'search_view',
                    ['id'],
                    unique=True)

    # create remaining indices on the tsv columns
    for index in index_set:
        op.create_index(op.f(
            'idx_tsv_{}'.format(index)),
            'search_view', [index],
            postgresql_using='gin'
        )

    # refresh materialzied view trigger
    conn.execute(sa.sql.text('''
        CREATE OR REPLACE FUNCTION trig_refresh_search_view() RETURNS trigger AS
        $$
        BEGIN
            REFRESH MATERIALIZED VIEW CONCURRENTLY search_view;
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
            EXECUTE PROCEDURE trig_refresh_search_view()
        '''.format(table=table, column=column)))


def downgrade():
    # grab a connection to the database
    conn = op.get_bind()
    # drop the materialized view
    conn.execute(sa.sql.text('''
        DROP MATERIALIZED VIEW search_view
    '''))
    for table, column in TRIGGER_TUPLES:
        conn.execute(sa.sql.text('''
            DROP TRIGGER IF EXISTS tsv_{table}_{column}_trigger ON {table}
        '''.format(table=table, column=column)))

