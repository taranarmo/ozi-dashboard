CREATE SCHEMA IF NOT EXISTS source;
CREATE SCHEMA IF NOT EXISTS data;

CREATE OR REPLACE FUNCTION data.set_timestamps()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        NEW.created := CURRENT_TIMESTAMP;
    END IF;
    NEW.updated := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


DROP TABLE IF EXISTS data.country;
CREATE TABLE data.country (
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    c_id SERIAL PRIMARY KEY,
    c_iso2 VARCHAR(2) NOT NULL,
    c_name VARCHAR(256) NOT NULL
);
CREATE TRIGGER trigger_set_timestamps_country
BEFORE INSERT OR UPDATE ON data.country
FOR EACH ROW
EXECUTE FUNCTION data.set_timestamps();


DROP TABLE IF EXISTS data.country_tag;
CREATE TABLE data.country_tag (
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ct_tag VARCHAR(32) NOT NULL,
    ct_country_id INT NOT NULL,
    PRIMARY KEY (ct_tag, ct_country_id),
    FOREIGN KEY (ct_country_id) REFERENCES data.country(c_id) ON DELETE CASCADE
    );
CREATE TRIGGER trigger_set_timestamps_country_tag
BEFORE INSERT OR UPDATE ON data.country_tag
FOR EACH ROW
EXECUTE FUNCTION data.set_timestamps();


DROP TABLE IF EXISTS data.asn;
CREATE TABLE data.asn (
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    a_id SERIAL PRIMARY KEY,
    a_country_iso2 VARCHAR(2) NOT NULL,
    a_ripe_id INTEGER NOT NULL
);
CREATE TRIGGER trigger_set_timestamps_asn
BEFORE INSERT OR UPDATE ON data.asn
FOR EACH ROW
EXECUTE FUNCTION data.set_timestamps();


DROP TABLE IF EXISTS data.country_stat;
CREATE TABLE data.country_stat (
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cs_id SERIAL PRIMARY KEY,
    cs_country_iso2 VARCHAR(2) NOT NULL,
    cs_stats_timestamp TIMESTAMP NOT NULL,
    cs_stats_resolution VARCHAR(4) NOT NULL,
    cs_v4_prefixes_ris INTEGER,
    cs_v6_prefixes_ris INTEGER,
    cs_asns_ris INTEGER,
    cs_v4_prefixes_stats INTEGER,
    cs_v6_prefixes_stats INTEGER,
    cs_asns_stats INTEGER
);
CREATE TRIGGER trigger_set_timestamps_country_stat
BEFORE INSERT OR UPDATE ON data.country_stat
FOR EACH ROW
EXECUTE FUNCTION data.set_timestamps();


DROP TABLE IF EXISTS source.ripe_api_load;
CREATE TABLE source.ripe_api_load (
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    r_id SERIAL PRIMARY KEY,
    r_url_used VARCHAR,
    r_response JSONB
);
CREATE TRIGGER trigger_set_timestamps_ripe_api_load
BEFORE INSERT OR UPDATE ON source.ripe_api_load
FOR EACH ROW
EXECUTE FUNCTION data.set_timestamps();


-- View for stats with resolution '1d'
CREATE OR REPLACE VIEW data.v_country_stat_1d AS
SELECT *
  FROM data.country_stat
 WHERE cs_stats_resolution = '1d';

-- View for stats with resolution '5m'
CREATE OR REPLACE VIEW data.v_country_stat_5m AS
SELECT *
  FROM data.country_stat
 WHERE cs_stats_resolution = '5m';
