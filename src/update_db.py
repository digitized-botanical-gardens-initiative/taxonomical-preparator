# import packages
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

CSV_PATH = f'{os.getcwd()}/data/out/test_inat_output.csv'

#create SQL query 
sql = f'''CREATE TEMP TABLE tmp_x (
        id NUMERIC,
        quality_grade VARCHAR(25),
        time_observed_at TIMESTAMP,
        taxon_geoprivacy VARCHAR(25),
        annotations VARCHAR(25),
        uuid TEXT,
        cached_votes_total BOOLEAN,
        identifications_most_agree BOOLEAN,
        species_guess VARCHAR(100),
        identifications_most_disagree BOOLEAN,
        tags VARCHAR(25),
        positional_accuracy NUMERIC,
        comments_count BOOLEAN,
        site_id BOOLEAN,
        license_code VARCHAR(25),
        quality_metrics TEXT,
        public_positional_accuracy NUMERIC,
        reviewed_by VARCHAR(60),
        oauth_application_id NUMERIC,
        flags VARCHAR(25),
        created_at TIMESTAMP,
        description TEXT,
        project_ids_with_curator_id VARCHAR(25),
        updated_at TIMESTAMP,
        sounds VARCHAR(25),
        place_ids VARCHAR(250),
        captive BOOLEAN,
        ident_taxon_ids TEXT,
        outlinks TEXT,
        faves_count BOOLEAN,
        ofvs TEXT,
        num_identification_agreements NUMERIC,
        comments TEXT,
        map_scale NUMERIC,
        uri VARCHAR(250),
        project_ids VARCHAR(25),
        community_taxon_id NUMERIC,
        owners_identification_from_vision BOOLEAN,
        identifications_count NUMERIC,
        obscured BOOLEAN,
        num_identification_disagreements BOOLEAN,
        geoprivacy BOOLEAN,
        location VARCHAR(100),
        votes TEXT,
        spam BOOLEAN,
        mappable BOOLEAN,
        identifications_some_agree BOOLEAN,
        project_ids_without_curator_id VARCHAR(25),
        place_guess TEXT,
        identifications TEXT,
        project_observations TEXT,
        photos TEXT,
        faves TEXT,
        non_owner_ids TEXT,
        observed_on TIMESTAMP,
        photo_url TEXT,
        "taxon.is_active" BOOLEAN,
        "taxon.ancestry" TEXT,
        "taxon.min_species_ancestry" TEXT,
        "taxon.endemic" BOOLEAN,
        "taxon.iconic_taxon_id" NUMERIC,
        "taxon.min_species_taxon_id" NUMERIC,
        "taxon.threatened" BOOLEAN,
        "taxon.rank_level" NUMERIC,
        "taxon.introduced" BOOLEAN,
        "taxon.native" BOOLEAN,
        "taxon.parent_id" NUMERIC,
        "taxon.name" VARCHAR(100),
        "taxon.rank" VARCHAR(25),
        "taxon.extinct" BOOLEAN,
        "taxon.id" NUMERIC,
        "taxon.ancestor_ids" TEXT,
        "taxon.photos_locked" BOOLEAN,
        "taxon.taxon_schemes_count" NUMERIC,
        "taxon.wikipedia_url" TEXT,
        "taxon.current_synonymous_taxon_ids" TEXT,
        "taxon.created_at" TIMESTAMP,
        "taxon.taxon_changes_count" NUMERIC,
        "taxon.complete_species_count" BOOLEAN,
        "taxon.universal_search_rank" NUMERIC,
        "taxon.observations_count" NUMERIC,
        "taxon.flag_counts.resolved" INTEGER,
        "taxon.flag_counts.unresolved" TEXT,
        "taxon.atlas_id" VARCHAR(50),
        "taxon.default_photo.id" NUMERIC,
        "taxon.default_photo.license_code" VARCHAR(25),
        "taxon.default_photo.attribution" TEXT,
        "taxon.default_photo.url" TEXT,
        "taxon.default_photo.original_dimensions.height" NUMERIC,
        "taxon.default_photo.original_dimensions.width" NUMERIC,
        "taxon.default_photo.flags" VARCHAR(25),
        "taxon.default_photo.square_url" TEXT,
        "taxon.default_photo.medium_url" TEXT,
        "taxon.iconic_taxon_name" VARCHAR(25),
        "taxon.preferred_common_name" VARCHAR(100),
        "preferences.prefers_community_taxon" BOOLEAN,
        "geojson.coordinates" VARCHAR(100),
        "geojson.type" VARCHAR(25),
        "user.site_id" NUMERIC,
        "user.created_at" TIMESTAMP,
        "user.id" NUMERIC,
        "user.login" VARCHAR(25),
        "user.spam" BOOLEAN,
        "user.suspended" BOOLEAN,
        "user.login_autocomplete" VARCHAR(25),
        "user.login_exact" VARCHAR(25),
        "user.name" VARCHAR(25),
        "user.name_autocomplete" VARCHAR(25),
        "user.orcid" BOOLEAN,
        "user.icon" TEXT,
        "user.observations_count" NUMERIC,
        "user.identifications_count" NUMERIC,
        "user.journal_posts_count" BOOLEAN,
        "user.activity_count" NUMERIC,
        "user.species_count" NUMERIC,
        "user.universal_search_rank" NUMERIC,
        "user.roles" VARCHAR(25),
        "user.icon_url" TEXT,
        "taxon.default_photo" BOOLEAN,
        "taxon.conservation_status.place_id" BOOLEAN,
        "taxon.conservation_status.source_id" NUMERIC,
        "taxon.conservation_status.user_id" BOOLEAN,
        "taxon.conservation_status.authority" VARCHAR(250),
        "taxon.conservation_status.status" VARCHAR(25),
        "taxon.conservation_status.status_name" VARCHAR(50),
        "taxon.conservation_status.geoprivacy" VARCHAR(50),
        "taxon.conservation_status.iucn" VARCHAR(25),
        observed_on_details BOOLEAN,
        created_time_zone VARCHAR(100),
        observed_time_zone VARCHAR(100),
        time_zone_offset VARCHAR(100),
        observed_on_string BOOLEAN,
        "created_at_details.date" TIMESTAMP,
        "created_at_details.week" NUMERIC,
        "created_at_details.month" NUMERIC,
        "created_at_details.hour" NUMERIC,
        "created_at_details.year" NUMERIC,
        "created_at_details.day" NUMERIC,
        swiped_loc VARCHAR(100),
        dbgi_id VARCHAR(50)
); -- but see below


COPY tmp_x FROM '{CSV_PATH}' delimiter ',' csv header;


ALTER TABLE tmp_x
ALTER COLUMN location
TYPE Geometry
USING ST_GeomFromText(replace(replace(replace(location,',',''),']',')'),'[','POINT('), 4326),
ALTER COLUMN swiped_loc
TYPE GEOMETRY 
USING ST_GeomFromText(replace(replace(replace(location,',',''),']',')'),'[','POINT('), 4326);

INSERT INTO pyinat
SELECT * FROM tmp_x
WHERE id NOT IN (SELECT id FROM pyinat);

UPDATE pyinat
SET     quality_grade = tmp_x.quality_grade ,
        time_observed_at = tmp_x.time_observed_at,
        taxon_geoprivacy = tmp_x.taxon_geoprivacy,
        annotations = tmp_x.annotations ,
        uuid = tmp_x.uuid ,
        cached_votes_total = tmp_x.cached_votes_total ,
        identifications_most_agree = tmp_x.identifications_most_agree ,
        species_guess = tmp_x.species_guess ,
        identifications_most_disagree = tmp_x.identifications_most_disagree ,
        tags = tmp_x.tags ,
        positional_accuracy = tmp_x.positional_accuracy ,
        comments_count = tmp_x.comments_count ,
        site_id = tmp_x.site_id,
        license_code = tmp_x.license_code ,
        quality_metrics = tmp_x.quality_metrics ,
        public_positional_accuracy = tmp_x.public_positional_accuracy ,
        reviewed_by = tmp_x.reviewed_by,
        oauth_application_id = tmp_x.oauth_application_id ,
        flags = tmp_x.flags ,
        created_at = tmp_x.created_at ,
        description = tmp_x.description ,
        project_ids_with_curator_id = tmp_x.project_ids_with_curator_id ,
        updated_at = tmp_x.updated_at ,
        sounds = tmp_x.sounds ,
        place_ids = tmp_x.place_ids ,
        captive = tmp_x.captive ,
        ident_taxon_ids = tmp_x.ident_taxon_ids ,
        outlinks = tmp_x.outlinks ,
        faves_count = tmp_x.faves_count ,
        ofvs = tmp_x.ofvs ,
        num_identification_agreements = tmp_x.num_identification_agreements ,
        comments = tmp_x.comments ,
        map_scale = tmp_x.map_scale ,
        uri = tmp_x.uri ,
        project_ids = tmp_x.project_ids ,
        community_taxon_id = tmp_x.community_taxon_id ,
        owners_identification_from_vision = tmp_x.owners_identification_from_vision ,
        identifications_count = tmp_x.identifications_count ,
        obscured = tmp_x.obscured ,
        num_identification_disagreements = tmp_x.num_identification_disagreements ,
        geoprivacy = tmp_x.geoprivacy ,
        location = tmp_x.location ,
        votes = tmp_x.votes ,
        spam = tmp_x.spam ,
        mappable = tmp_x.mappable ,
        identifications_some_agree = tmp_x.identifications_some_agree ,
        project_ids_without_curator_id = tmp_x.project_ids_without_curator_id ,
        place_guess = tmp_x.place_guess ,
        identifications = tmp_x.identifications ,
        project_observations = tmp_x.project_observations ,
        photos = tmp_x.photos ,
        faves = tmp_x.faves ,
        non_owner_ids = tmp_x.non_owner_ids ,
        observed_on = tmp_x.observed_on ,
        photo_url = tmp_x.photo_url ,
        "taxon.is_active" = tmp_x."taxon.is_active" ,
        "taxon.ancestry" = tmp_x."taxon.ancestry",
        "taxon.min_species_ancestry" = tmp_x."taxon.min_species_ancestry"  ,
        "taxon.endemic" = tmp_x."taxon.endemic" ,
        "taxon.iconic_taxon_id" = tmp_x."taxon.iconic_taxon_id" ,
        "taxon.min_species_taxon_id" = tmp_x."taxon.min_species_taxon_id" ,
        "taxon.threatened" = tmp_x."taxon.threatened" ,
        "taxon.rank_level" = tmp_x."taxon.rank_level" ,
        "taxon.introduced" = tmp_x."taxon.introduced",
        "taxon.native" = tmp_x."taxon.native" ,
        "taxon.parent_id" = tmp_x."taxon.parent_id" ,
        "taxon.name" = tmp_x."taxon.name" ,
        "taxon.rank" = tmp_x."taxon.rank" ,
        "taxon.extinct" = tmp_x."taxon.extinct" ,
        "taxon.id" = tmp_x."taxon.id" ,
        "taxon.ancestor_ids" = tmp_x."taxon.ancestor_ids" ,
        "taxon.photos_locked" = tmp_x."taxon.photos_locked" ,
        "taxon.taxon_schemes_count" = tmp_x."taxon.taxon_schemes_count" ,
        "taxon.wikipedia_url" = tmp_x."taxon.wikipedia_url" ,
        "taxon.current_synonymous_taxon_ids" = tmp_x."taxon.current_synonymous_taxon_ids" ,
        "taxon.created_at" = tmp_x."taxon.created_at" ,
        "taxon.taxon_changes_count" = tmp_x."taxon.taxon_changes_count" ,
        "taxon.complete_species_count" = tmp_x."taxon.complete_species_count" ,
        "taxon.universal_search_rank" = tmp_x."taxon.universal_search_rank" ,
        "taxon.observations_count" = tmp_x."taxon.observations_count" ,
        "taxon.flag_counts.resolved" = tmp_x."taxon.flag_counts.resolved" ,
        "taxon.flag_counts.unresolved" = tmp_x."taxon.flag_counts.unresolved" ,
        "taxon.atlas_id" = tmp_x."taxon.atlas_id" ,
        "taxon.default_photo.id" = tmp_x."taxon.default_photo.id",
        "taxon.default_photo.license_code" = tmp_x."taxon.default_photo.license_code" ,
        "taxon.default_photo.attribution" = tmp_x."taxon.default_photo.attribution" ,
        "taxon.default_photo.url" = tmp_x."taxon.default_photo.url" ,
        "taxon.default_photo.original_dimensions.height" = tmp_x."taxon.default_photo.original_dimensions.height" ,
        "taxon.default_photo.original_dimensions.width" = tmp_x."taxon.default_photo.original_dimensions.width",
        "taxon.default_photo.flags" = tmp_x."taxon.default_photo.flags" ,
        "taxon.default_photo.square_url" = tmp_x."taxon.default_photo.square_url",
        "taxon.default_photo.medium_url" = tmp_x."taxon.default_photo.medium_url" ,
        "taxon.iconic_taxon_name" = tmp_x."taxon.iconic_taxon_name" ,
        "taxon.preferred_common_name" = tmp_x."taxon.preferred_common_name",
        "preferences.prefers_community_taxon" = tmp_x."preferences.prefers_community_taxon" ,
        "geojson.coordinates" = tmp_x."geojson.coordinates",
        "geojson.type" = tmp_x."geojson.type" ,
        "user.site_id" = tmp_x."user.site_id" ,
        "user.created_at" = tmp_x."user.created_at" ,
        "user.id" = tmp_x."user.id" ,
        "user.login" = tmp_x."user.login" ,
        "user.spam" = tmp_x."user.spam" ,
        "user.suspended" = tmp_x."user.suspended" ,
        "user.login_autocomplete" = tmp_x."user.login_autocomplete",
        "user.login_exact" = tmp_x."user.login_exact" ,
        "user.name" = tmp_x."user.name" ,
        "user.name_autocomplete" = tmp_x."user.name_autocomplete" ,
        "user.orcid" = tmp_x."user.orcid" ,
        "user.icon" = tmp_x."user.icon" ,
        "user.observations_count" = tmp_x."user.observations_count" ,
        "user.identifications_count" = tmp_x."user.identifications_count" ,
        "user.journal_posts_count" = tmp_x."user.journal_posts_count" ,
        "user.activity_count" = tmp_x."user.activity_count" ,
        "user.species_count" = tmp_x."user.species_count" ,
        "user.universal_search_rank" = tmp_x."user.universal_search_rank" ,
        "user.roles" = tmp_x."user.roles" ,
        "user.icon_url" = tmp_x."user.icon_url" ,
        "taxon.default_photo" = tmp_x."taxon.default_photo" ,
        "taxon.conservation_status.place_id" = tmp_x."taxon.conservation_status.place_id" ,
        "taxon.conservation_status.source_id" = tmp_x."taxon.conservation_status.source_id" ,
        "taxon.conservation_status.user_id" = tmp_x."taxon.conservation_status.user_id" ,
        "taxon.conservation_status.authority" = tmp_x."taxon.conservation_status.authority" ,
        "taxon.conservation_status.status" = tmp_x."taxon.conservation_status.status" ,
        "taxon.conservation_status.status_name" = tmp_x."taxon.conservation_status.status_name" ,
        "taxon.conservation_status.geoprivacy" = tmp_x."taxon.conservation_status.geoprivacy" ,
        "taxon.conservation_status.iucn" = tmp_x."taxon.conservation_status.iucn" ,
        observed_on_details = tmp_x.observed_on_details ,
        created_time_zone = tmp_x.created_time_zone ,
        observed_time_zone = tmp_x.observed_time_zone ,
        time_zone_offset = tmp_x.time_zone_offset ,
        observed_on_string = tmp_x.observed_on_string ,
        "created_at_details.date" = tmp_x."created_at_details.date" ,
        "created_at_details.week" = tmp_x."created_at_details.week" ,
        "created_at_details.month" = tmp_x."created_at_details.month" ,
        "created_at_details.hour" = tmp_x."created_at_details.hour" ,
        "created_at_details.year" = tmp_x."created_at_details.year" ,
        "created_at_details.day" = tmp_x."created_at_details.day" ,
        swiped_loc = tmp_x.swiped_loc,
        dbgi_id = tmp_x.dbgi_id
FROM tmp_x  
WHERE pyinat.id = tmp_x.id 
        ;



DROP TABLE tmp_x; -- else it is dropped at end of session automatically'''

# import env variable
load_dotenv()

usr=os.getenv('DB_USR')
pwd=os.getenv('DIRECTUS_PWD')


# establish connections

#conn_string = 'postgresql://directus:directus_dbgi@127.0.0.1/directus_dbgi'
#db = create_engine(conn_string)
#conn = db.connect()

conn1 = psycopg2.connect(
	database="directus_dbgi",
    user=usr,
    password=pwd,
    host='127.0.0.1',
    port= '5432'
    )

#conn1.autocommit = True

# execute query
cursor = conn1.cursor()
cursor.execute(sql)

# commit and close connection
conn1.commit()
conn1.close()
