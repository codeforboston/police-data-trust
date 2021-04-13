-- public.incidents definition

-- Drop table

-- DROP TABLE public.incidents;

DROP TYPE IF EXISTS cause_of_death_enum cascade;


CREATE TYPE cause_of_death_enum AS ENUM (
	'Unknown',
	'BluntForce',
	'GunShot',
	'Choke',
	'Other');

DROP TYPE IF EXISTS gender_enum cascade;

CREATE TYPE gender_enum AS ENUM (
	'Unknown',
	'Male',
	'Female',
	'Transgender');

DROP TYPE IF EXISTS initial_encounter_enum cascade;

CREATE TYPE initial_encounter_enum AS ENUM (
	'Unknown',
	'TrafficViolation',
	'Trespassing',
	'PotentialCrimeSuspect',
	'Other');

DROP TYPE IF EXISTS race_enum cascade;

CREATE TYPE race_enum AS ENUM (
	'Unknown',
	'White',
	'Black_African_American',
	'American_Indian_Alaska_Native',
	'Asian',
	'Native_Hawaiian_Pacific_Islander');

DROP TYPE IF EXISTS status_enum cascade;

CREATE TYPE status_enum AS ENUM (
	'Unknown',
	'Unharmed',
	'Injured',
	'Disabled',
	'Deceased');

DROP TYPE IF EXISTS victim_action_enum cascade;

CREATE TYPE victim_action_enum AS ENUM (
	'Unknown',
	'Speaking',
	'NoAction',
	'Fleeing',
	'Approaching',
	'Attacking',
	'Other');

DROP TYPE IF EXISTS victim_weapon_enum cascade;

CREATE TYPE victim_weapon_enum AS ENUM (
	'Unknown',
	'Firearm',
	'Blade',
	'Blunt',
	'NoWeapon',
	'Other');

DROP TABLE IF EXISTS public.incidents;
CREATE TABLE public.incidents (
	"incident_id" serial NOT NULL,
	"occurrence_date" timestamp NULL,
	"state_abbv" text NULL,
	"city" text NULL,
	"address_1" text NULL,
	"address_2" text NULL,
	"zip_code" text NULL,
	"latitude" float8 NULL,
	"longitude" float8 NULL,
	"reported_date" timestamp NULL,
	"initial_reason_for_encounter" initial_encounter_enum NULL,
	"charges_involved" text NULL,
	"victim_weapon" victim_weapon_enum NULL,
	"victim_action" victim_action_enum NULL,
	"has_multimedia" bool NULL,
	"media_URL" text NULL,
	"from_report" bool NULL,
	"description" text NULL,
	"associated_incidents" text NULL,
	"death_date" timestamp NULL,
	"death_state_abbv" text NULL,
	"death_city" text NULL,
	"death_address_1" text NULL,
	"death_address_2" text NULL,
	"death_zip_code" text NULL,
	"cause_of_death" cause_of_death_enum NULL,
	"cause_of_death_description" text NULL,
	"first_name" text NULL,
	"last_name" text NULL,
	"age_at_incident" int4 NULL,
	"gender" gender_enum NULL,
	"race" race_enum NULL,
	"status" status_enum NULL,
	"agency_id" int4 NULL,
	"agency_name" text NULL,
	"agency_state_abbv" text NULL,
	"agency_city" text NULL,
	"agency_address_1" text NULL,
	"agency_address_2" text NULL,
	"agency_zip_code" text NULL,
	"agency_latitude" float8 NULL,
	"agency_longitude" float8 NULL,
	CONSTRAINT incidents_pkey PRIMARY KEY ("incident_id")
);


INSERT INTO public.incidents
("incident_id", "occurrence_date", "state_abbv", "city", "address_1", "address_2", "zip_code", "latitude", "longitude", "reported_date", "initial_reason_for_encounter", "charges_involved", "victim_weapon", "victim_action", "has_multimedia", "media_URL", "from_report", "description", "associated_incidents", "death_date", "death_state_abbv", "death_city", "death_address_1", "death_address_2", "death_zip_code", "cause_of_death", "cause_of_death_description", "first_name", "last_name", "age_at_incident", "gender", "race", "status", "agency_id", "agency_name", "agency_state_abbv", "agency_city", "agency_address_1", "agency_address_2", "agency_zip_code", "agency_latitude", "agency_longitude")
VALUES(1, '2021-03-01 00:00:00.000', 'MA', 'Boston', '1 Commonwealth Ave', '', '02215', NULL, NULL, NULL, 'Trespassing'::initial_encounter_enum::initial_encounter_enum, 'None', 'Firearm'::victim_weapon_enum::victim_weapon_enum, 'Fleeing'::victim_action_enum::victim_action_enum, false, NULL, true, 'This is an example incident description', NULL, '2020-04-01 00:00:00.000', 'MA', 'Boston', '120 Ward St', NULL, '02120', 'BluntForce'::cause_of_death_enum::cause_of_death_enum, NULL, 'Jane', 'Smith', 25, 'Female'::gender_enum::gender_enum, 'Black_African_American'::race_enum::race_enum, 'Deceased'::status_enum::status_enum, NULL, 'Boston Police Department', 'MA', 'Boston', '1 Schroder Plaza', NULL, '02120', 42.3339686, -71.0907954);

INSERT INTO public.incidents
("incident_id", "occurrence_date", "state_abbv", "city", "address_1", "address_2", "zip_code", "latitude", "longitude", "reported_date", "initial_reason_for_encounter", "charges_involved", "victim_weapon", "victim_action", "has_multimedia", "media_URL", "from_report", "description", "associated_incidents", "death_date", "death_state_abbv", "death_city", "death_address_1", "death_address_2", "death_zip_code", "cause_of_death", "cause_of_death_description", "first_name", "last_name", "age_at_incident", "gender", "race", "status", "agency_id", "agency_name", "agency_state_abbv", "agency_city", "agency_address_1", "agency_address_2", "agency_zip_code", "agency_latitude", "agency_longitude")
VALUES(2, '2021-03-26 00:00:00.000', 'MA', 'Allston', '1000 Commonwealth Ave', 'Apt 101', '02215', 42.3539, 71.1337, '2020-02-20 00:00:00.000', 'TrafficViolation'::initial_encounter_enum::initial_encounter_enum, 'Arrest', 'Blunt'::victim_weapon_enum::victim_weapon_enum, 'Speaking'::victim_action_enum::victim_action_enum, false, '', false, 'lorem ipsum sit dolor amet', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'John', 'Doe', 30, 'Male'::gender_enum::gender_enum, 'Unknown'::race_enum::race_enum, 'Injured'::status_enum::status_enum, 10, 'Boston Police Department', 'MA', 'Boston', '1 Schroeder Plaza', '', '02120', 42.3339686, -71.0907954);
