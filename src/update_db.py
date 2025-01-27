# import packages
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

#Get the path to the output of inaturalist
CSV_PATH = f'{os.getcwd()}/data/out/test_inat_output.csv'

#create SQL query 
sql = f'''
/* Create a temporary table with the columns found in the csv file 
and copy the values from the csv file
*/

CREATE TEMP TABLE tmp_x (
        id NUMERIC,
        quality_grade VARCHAR(25),
        time_observed_at TIMESTAMP,
        taxon_geoprivacy VARCHAR(25),
        annotations VARCHAR(25),
        uuid TEXT,
        cached_votes_total NUMERIC,
        identifications_most_agree BOOLEAN,
        species_guess VARCHAR(100),
        identifications_most_disagree BOOLEAN,
        tags VARCHAR(150),
        positional_accuracy NUMERIC,
        comments_count NUMERIC,
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
        faves_count NUMERIC,
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
        num_identification_disagreements NUMERIC,
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
        taxon_is_active BOOLEAN,
        taxon_ancestry TEXT,
        taxon_min_species_ancestry TEXT,
        taxon_endemic BOOLEAN,
        taxon_iconic_taxon_id NUMERIC,
        taxon_min_species_taxon_id NUMERIC,
        taxon_threatened BOOLEAN,
        taxon_rank_level NUMERIC,
        taxon_introduced BOOLEAN,
        taxon_native BOOLEAN,
        taxon_parent_id NUMERIC,
        taxon_name VARCHAR(100),
        taxon_rank VARCHAR(25),
        taxon_extinct BOOLEAN,
        taxon_id NUMERIC,
        taxon_ancestor_ids TEXT,
        taxon_photos_locked BOOLEAN,
        taxon_taxon_schemes_count NUMERIC,
        taxon_wikipedia_url TEXT,
        taxon_current_synonymous_taxon_ids TEXT,
        taxon_created_at TIMESTAMP,
        taxon_taxon_changes_count NUMERIC,
        taxon_complete_species_count BOOLEAN,
        taxon_universal_search_rank NUMERIC,
        taxon_observations_count NUMERIC,
        taxon_flag_counts_resolved NUMERIC,
        taxon_flag_counts_unresolved NUMERIC,
        taxon_atlas_id VARCHAR(50),
        taxon_default_photo_id NUMERIC,
        taxon_default_photo_license_code VARCHAR(25),
        taxon_default_photo_attribution TEXT,
        taxon_default_photo_url TEXT,
        taxon_default_photo_original_dimensions_height NUMERIC,
        taxon_default_photo_original_dimensions_width NUMERIC,
        taxon_default_photo_flags TEXT,
        taxon_default_photo_square_url TEXT,
        taxon_default_photo_medium_url TEXT,
        taxon_iconic_taxon_name VARCHAR(25),
        taxon_preferred_common_name VARCHAR(100),
        preferences_prefers_community_taxon BOOLEAN,
        geojson_coordinates VARCHAR(100),
        geojson_type VARCHAR(25),
        user_site_id NUMERIC,
        user_created_at TIMESTAMP,
        user_id NUMERIC,
        user_login VARCHAR(25),
        user_spam BOOLEAN,
        user_suspended BOOLEAN,
        user_login_autocomplete VARCHAR(25),
        user_login_exact VARCHAR(25),
        user_name VARCHAR(25),
        user_name_autocomplete VARCHAR(25),
        user_orcid BOOLEAN,
        user_icon TEXT,
        user_observations_count NUMERIC,
        user_identifications_count NUMERIC,
        user_journal_posts_count NUMERIC,
        user_activity_count NUMERIC,
        user_species_count NUMERIC,
        user_universal_search_rank NUMERIC,
        user_roles VARCHAR(25),
        user_icon_url TEXT,
        taxon_default_photo BOOLEAN,
        taxon_conservation_status_place_id BOOLEAN,
        taxon_conservation_status_source_id NUMERIC,
        taxon_conservation_status_user_id BOOLEAN,
        taxon_conservation_status_authority VARCHAR(250),
        taxon_conservation_status_status VARCHAR(25),
        taxon_conservation_status_status_name VARCHAR(50),
        taxon_conservation_status_geoprivacy VARCHAR(50),
        taxon_conservation_status_iucn VARCHAR(25),
        observed_on_details BOOLEAN,
        created_time_zone VARCHAR(100),
        observed_time_zone VARCHAR(100),
        time_zone_offset VARCHAR(100),
        observed_on_string BOOLEAN,
        created_at_details_date TIMESTAMP,
        created_at_details_week NUMERIC,
        created_at_details_month NUMERIC,
        created_at_details_hour NUMERIC,
        created_at_details_year NUMERIC,
        created_at_details_day NUMERIC,
        swiped_loc VARCHAR(100),
        emi_external_id VARCHAR(50)
); -- but see below


COPY tmp_x FROM '{CSV_PATH}' delimiter ',' csv header;

--Alter the table to format the location and the swiped_loc columns as a geometry type

ALTER TABLE tmp_x
ADD COLUMN updated_on TIMESTAMP,
ALTER COLUMN location
TYPE Geometry
USING ST_GeomFromText(replace(replace(replace(location,',',''),']',')'),'[','POINT('), 4326),
ALTER COLUMN geojson_coordinates
TYPE GEOMETRY 
USING ST_GeomFromText(replace(replace(replace(geojson_coordinates,',',''),']',')'),'[','POINT('), 4326),
ALTER COLUMN swiped_loc
TYPE GEOMETRY 
USING ST_GeomFromText(replace(replace(swiped_loc,',',''),'(','POINT('), 4326);


--Insert the values from the temporary table in the pyinat table where the ids do not already exist

INSERT INTO pyinat
SELECT * FROM tmp_x
WHERE id NOT IN (SELECT id FROM pyinat);

--Update the values of the columns where the ids already exist and match

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
        taxon_is_active = tmp_x.taxon_is_active ,
        taxon_ancestry = tmp_x.taxon_ancestry,
        taxon_min_species_ancestry = tmp_x.taxon_min_species_ancestry  ,
        taxon_endemic = tmp_x.taxon_endemic ,
        taxon_iconic_taxon_id = tmp_x.taxon_iconic_taxon_id ,
        taxon_min_species_taxon_id = tmp_x.taxon_min_species_taxon_id ,
        taxon_threatened = tmp_x.taxon_threatened ,
        taxon_rank_level = tmp_x.taxon_rank_level ,
        taxon_introduced = tmp_x.taxon_introduced,
        taxon_native = tmp_x.taxon_native ,
        taxon_parent_id = tmp_x.taxon_parent_id ,
        taxon_name = tmp_x.taxon_name ,
        taxon_rank = tmp_x.taxon_rank ,
        taxon_extinct = tmp_x.taxon_extinct ,
        taxon_id = tmp_x.taxon_id ,
        taxon_ancestor_ids = tmp_x.taxon_ancestor_ids ,
        taxon_photos_locked = tmp_x.taxon_photos_locked ,
        taxon_taxon_schemes_count = tmp_x.taxon_taxon_schemes_count ,
        taxon_wikipedia_url = tmp_x.taxon_wikipedia_url ,
        taxon_current_synonymous_taxon_ids = tmp_x.taxon_current_synonymous_taxon_ids ,
        taxon_created_at = tmp_x.taxon_created_at ,
        taxon_taxon_changes_count = tmp_x.taxon_taxon_changes_count ,
        taxon_complete_species_count = tmp_x.taxon_complete_species_count ,
        taxon_universal_search_rank = tmp_x.taxon_universal_search_rank ,
        taxon_observations_count = tmp_x.taxon_observations_count ,
        taxon_flag_counts_resolved = tmp_x.taxon_flag_counts_resolved ,
        taxon_flag_counts_unresolved = tmp_x.taxon_flag_counts_unresolved ,
        taxon_atlas_id = tmp_x.taxon_atlas_id ,
        taxon_default_photo_id = tmp_x.taxon_default_photo_id,
        taxon_default_photo_license_code = tmp_x.taxon_default_photo_license_code ,
        taxon_default_photo_attribution = tmp_x.taxon_default_photo_attribution ,
        taxon_default_photo_url = tmp_x.taxon_default_photo_url ,
        taxon_default_photo_original_dimensions_height = tmp_x.taxon_default_photo_original_dimensions_height ,
        taxon_default_photo_original_dimensions_width = tmp_x.taxon_default_photo_original_dimensions_width,
        taxon_default_photo_flags = tmp_x.taxon_default_photo_flags ,
        taxon_default_photo_square_url = tmp_x.taxon_default_photo_square_url,
        taxon_default_photo_medium_url = tmp_x.taxon_default_photo_medium_url ,
        taxon_iconic_taxon_name = tmp_x.taxon_iconic_taxon_name ,
        taxon_preferred_common_name = tmp_x.taxon_preferred_common_name,
        preferences_prefers_community_taxon = tmp_x.preferences_prefers_community_taxon ,
        geojson_coordinates = tmp_x.geojson_coordinates,
        geojson_type = tmp_x.geojson_type ,
        user_site_id = tmp_x.user_site_id ,
        user_created_at = tmp_x.user_created_at ,
        user_id = tmp_x.user_id ,
        user_login = tmp_x.user_login ,
        user_spam = tmp_x.user_spam ,
        user_suspended = tmp_x.user_suspended ,
        user_login_autocomplete = tmp_x.user_login_autocomplete,
        user_login_exact = tmp_x.user_login_exact ,
        user_name = tmp_x.user_name ,
        user_name_autocomplete = tmp_x.user_name_autocomplete ,
        user_orcid = tmp_x.user_orcid ,
        user_icon = tmp_x.user_icon ,
        user_observations_count = tmp_x.user_observations_count ,
        user_identifications_count = tmp_x.user_identifications_count ,
        user_journal_posts_count = tmp_x.user_journal_posts_count ,
        user_activity_count = tmp_x.user_activity_count ,
        user_species_count = tmp_x.user_species_count ,
        user_universal_search_rank = tmp_x.user_universal_search_rank ,
        user_roles = tmp_x.user_roles ,
        user_icon_url = tmp_x.user_icon_url ,
        taxon_default_photo = tmp_x.taxon_default_photo ,
        taxon_conservation_status_place_id = tmp_x.taxon_conservation_status_place_id ,
        taxon_conservation_status_source_id = tmp_x.taxon_conservation_status_source_id ,
        taxon_conservation_status_user_id = tmp_x.taxon_conservation_status_user_id ,
        taxon_conservation_status_authority = tmp_x.taxon_conservation_status_authority ,
        taxon_conservation_status_status = tmp_x.taxon_conservation_status_status ,
        taxon_conservation_status_status_name = tmp_x.taxon_conservation_status_status_name ,
        taxon_conservation_status_geoprivacy = tmp_x.taxon_conservation_status_geoprivacy ,
        taxon_conservation_status_iucn = tmp_x.taxon_conservation_status_iucn ,
        observed_on_details = tmp_x.observed_on_details ,
        created_time_zone = tmp_x.created_time_zone ,
        observed_time_zone = tmp_x.observed_time_zone ,
        time_zone_offset = tmp_x.time_zone_offset ,
        observed_on_string = tmp_x.observed_on_string ,
        created_at_details_date = tmp_x.created_at_details_date ,
        created_at_details_week = tmp_x.created_at_details_week ,
        created_at_details_month = tmp_x.created_at_details_month ,
        created_at_details_hour = tmp_x.created_at_details_hour ,
        created_at_details_year = tmp_x.created_at_details_year ,
        created_at_details_day = tmp_x.created_at_details_day ,
        swiped_loc = tmp_x.swiped_loc,
        emi_external_id = tmp_x.emi_external_id
FROM tmp_x  
WHERE pyinat.id = tmp_x.id 
        ;

--Drop the temporary table
DROP TABLE tmp_x; -- else it is dropped at end of session automatically

'''

# import env variable
load_dotenv()

usr=os.getenv('DB_USR')
pwd=os.getenv('DIRECTUS_PWD')


# establish connections

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
