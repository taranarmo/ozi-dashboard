-- first things first
-- uncomment and run
-- CREATE DATABASE asn_stats;

-- switch to asn_stats database before proceeding;
-- CREATE USER asn_stats WITH PASSWORD 'change-this-one-before-running-the-query';
-- GRANT ALL PRIVILEGES ON DATABASE asn_stats TO asn_stats;

-- re-login with asn_stats user before proceeding
-- CREATE SCHEMA source;
-- CREATE SCHEMA dwh;
-- CREATE SCHEMA present;

CREATE OR REPLACE FUNCTION dwh.set_timestamps()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        NEW.created := CURRENT_TIMESTAMP;
    END IF;

    NEW.updated := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TABLE IF EXISTS dwh.country;
CREATE TABLE dwh.country (
    created TIMESTAMP,
    updated TIMESTAMP,
    c_id SERIAL PRIMARY KEY,
    c_iso2 VARCHAR(2),
    cname VARCHAR(32)
);

CREATE TRIGGER set_timestamps_trigger_country
BEFORE INSERT OR UPDATE ON dwh.country
FOR EACH ROW
EXECUTE FUNCTION dwh.set_timestamps();

DROP TABLE IF EXISTS dwh.asn;
CREATE TABLE dwh.asn (
    created TIMESTAMP,
    updated TIMESTAMP,
    a_id SERIAL PRIMARY KEY,
    a_country_iso2 VARCHAR(2),
    a_ripe_id INTEGER
);

CREATE TRIGGER set_timestamps_trigger_asn
BEFORE INSERT OR UPDATE ON dwh.country
FOR EACH ROW
EXECUTE FUNCTION dwh.set_timestamps();

DROP TABLE IF EXISTS dwh.country_stat;
CREATE TABLE dwh.country_stat (
    created TIMESTAMP,
    updated TIMESTAMP,
    cs_id SERIAL PRIMARY KEY,
    cs_created TIMESTAMP,
    cs_updated TIMESTAMP,
    cs_country_iso2 VARCHAR(2),
    cs_stats_date TIMESTAMP,
    cs_v4_prefixes_ris INTEGER,
    cs_v6_prefixes_ris INTEGER,
    cs_asns_ris INTEGER,
    cs_v4_prefixes_stats INTEGER,
    cs_v6_prefixes_stats INTEGER,
    cs_asns_stats INTEGER
);

CREATE TRIGGER set_timestamps_trigger_country_stat
BEFORE INSERT OR UPDATE ON dwh.country_stat
FOR EACH ROW
EXECUTE FUNCTION dwh.set_timestamps();

DROP TABLE IF EXISTS source.ripe_api_load;
CREATE TABLE source.ripe_api_load (
    created TIMESTAMP,
    updated TIMESTAMP,
    r_id SERIAL PRIMARY KEY,
    r_url_used VARCHAR,
    r_response JSONB
);

CREATE TRIGGER set_timestamps_trigger_ripe_api_load
BEFORE INSERT OR UPDATE ON source.ripe_api_load
FOR EACH ROW
EXECUTE FUNCTION dwh.set_timestamps();