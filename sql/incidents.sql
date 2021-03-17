-- police_data.incidents definition

-- Drop table

DROP TABLE police_data.incidents;
DROP TYPE cause_of_death_enum;

CREATE TYPE cause_of_death_enum AS ENUM (
	'Unknown',
	'BluntForce',
	'GunShot',
	'Choke',
	'Other');

DROP TYPE gender_enum;

CREATE TYPE gender_enum AS ENUM (
	'Unknown',
	'Male',
	'Female',
	'Transgender');

DROP TYPE initial_encounter_enum;

CREATE TYPE initial_encounter_enum AS ENUM (
	'Unknown',
	'TrafficViolation',
	'Trespassing',
	'PotentialCrimeSuspect',
	'Other');

DROP TYPE race_enum;

CREATE TYPE race_enum AS ENUM (
	'Unknown',
	'White',
	'Black_African_American',
	'American_Indian_Alaska_Native',
	'Asian',
	'Native_Hawaiian_Pacific_Islander');

DROP TYPE status_enum;

CREATE TYPE status_enum AS ENUM (
	'Unknown',
	'Unharmed',
	'Injured',
	'Disabled',
	'Deceased');

DROP TYPE victim_action_enum;

CREATE TYPE victim_action_enum AS ENUM (
	'Unknown',
	'Speaking',
	'NoAction',
	'Fleeing',
	'Approaching',
	'Attacking',
	'Other');

DROP TYPE victim_weapon_enum;

CREATE TYPE victim_weapon_enum AS ENUM (
	'Unknown',
	'Firearm',
	'Blade',
	'Blunt',
	'NoWeapon',
	'Other');


CREATE TABLE police_data.incidents (
	"Incident_ID" serial NOT NULL,
	"Occurrence_Date" timestamp NULL,
	"State_Abbv" text NULL,
	"City" text NULL,
	"Address_1" text NULL,
	"Address_2" text NULL,
	"Zip_Code" text NULL,
	"Latitude" float8 NULL,
	"Longitude" float8 NULL,
	"Reported_Date" timestamp NULL,
	"Initial_Reason_For_Encounter" initial_encounter_enum NULL,
	"Charges_Involved" text NULL,
	"Victim_Weapon" victim_weapon_enum NULL,
	"Victim_Action" victim_action_enum NULL,
	"Has_Multimedia" bool NULL,
	"Media_URL" text NULL,
	"From_Report" bool NULL,
	"Description" text NULL,
	"Associated_Incidents" text NULL,
	"Death_Date" timestamp NULL,
	"Death_State_Abbv" text NULL,
	"Death_City" text NULL,
	"Death_Address_1" text NULL,
	"Death_Address_2" text NULL,
	"Death_Zip_Code" text NULL,
	"Cause_Of_Death" cause_of_death_enum NULL,
	"Cause_Of_Death_Description" text NULL,
	"First_Name" text NULL,
	"Last_Name" text NULL,
	"Age_At_Incident" int4 NULL,
	"Gender" gender_enum NULL,
	"Race" race_enum NULL,
	"Status" status_enum NULL,
	"Agency_ID" int4 NULL,
	"Agency_Name" text NULL,
	"Agency_State_Abbv" text NULL,
	"Agency_City" text NULL,
	"Agency_Address_1" text NULL,
	"Agency_Address_2" text NULL,
	"Agency_Zip_Code" text NULL,
	"Agency_Latitude" float8 NULL,
	"Agency_Longitude" float8 NULL,
	CONSTRAINT incidents_pkey PRIMARY KEY ("Incident_ID")
);

INSERT INTO police_data.incidents ("Occurrence_Date","State_Abbv","City","Address_1","Address_2","Zip_Code","Latitude","Longitude","Reported_Date","Initial_Reason_For_Encounter","Charges_Involved","Victim_Weapon","Victim_Action","Has_Multimedia","Media_URL","From_Report","Description","Associated_Incidents","Death_Date","Death_State_Abbv","Death_City","Death_Address_1","Death_Address_2","Death_Zip_Code","Cause_Of_Death","Cause_Of_Death_Description","First_Name","Last_Name","Age_At_Incident","Gender","Race","Status","Agency_ID","Agency_Name","Agency_State_Abbv","Agency_City","Agency_Address_1","Agency_Address_2","Agency_Zip_Code","Agency_Latitude","Agency_Longitude") VALUES
	 ('2021-03-01 00:00:00.000','MA','Boston','1 Commonwealth Ave','','02215',NULL,NULL,NULL,'Trespassing'::initial_encounter_enum::initial_encounter_enum,'None','Firearm'::victim_weapon_enum::victim_weapon_enum,'Fleeing'::victim_action_enum::victim_action_enum,false,NULL,true,'This is an example incident description',NULL,'2020-04-01 00:00:00.000','MA','Boston','120 Ward St',NULL,'02120','BluntForce'::cause_of_death_enum::cause_of_death_enum,NULL,'Jane','Smith',25,'Female'::gender_enum::gender_enum,'Black_African_American'::race_enum::race_enum,'Deceased'::status_enum::status_enum,NULL,'Boston Police Department','MA','Boston','1 Schroder Plaza',NULL,'02120',42.3339686,-71.0907954);

INSERT INTO police_data.incidents ("Occurrence_Date","State_Abbv","City","Address_1","Address_2","Zip_Code","Latitude","Longitude","Reported_Date","Initial_Reason_For_Encounter","Charges_Involved","Victim_Weapon","Victim_Action","Has_Multimedia","Media_URL","From_Report","Description","Associated_Incidents","Death_Date","Death_State_Abbv","Death_City","Death_Address_1","Death_Address_2","Death_Zip_Code","Cause_Of_Death","Cause_Of_Death_Description","First_Name","Last_Name","Age_At_Incident","Gender","Race","Status","Agency_ID","Agency_Name","Agency_State_Abbv","Agency_City","Agency_Address_1","Agency_Address_2","Agency_Zip_Code","Agency_Latitude","Agency_Longitude") VALUES
	 ('2021-03-26 00:00:00.000','MA','Allston','1000 Commonwealth Ave','Apt 101','02215',42.3539,71.1337,'2020-02-20 00:00:00.000','TrafficViolation'::initial_encounter_enum::initial_encounter_enum,'Arrest','Blunt'::victim_weapon_enum::victim_weapon_enum,'Speaking'::victim_action_enum::victim_action_enum,false,'',false,'lorem ipsum sit dolor amet',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'John','Doe',30,'Male'::gender_enum::gender_enum,'Unknown'::race_enum::race_enum,'Injured'::status_enum::status_enum,10,'Boston Police Department','MA','Boston','1 Schroeder Plaza','','02120',42.3339686,-71.0907954);