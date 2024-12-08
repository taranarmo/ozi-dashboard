


-- View for stats with resolution '1d'
CREATE OR REPLACE VIEW data.v_country_stat_1d AS
SELECT data.country_stat.*, data.country.c_name
  FROM data.country_stat
  JOIN data.country on c_iso2 = cs_country_iso2
 WHERE cs_stats_resolution = '1d';

-- View for stats with resolution '5m'
CREATE OR REPLACE VIEW data.v_country_stat_5m AS
SELECT data.country_stat.*, data.country.c_name
  FROM data.country_stat
  JOIN data.country on c_iso2 = cs_country_iso2
 WHERE cs_stats_resolution = '5m';

-- View for last stats available for the country
CREATE OR REPLACE VIEW data.v_country_stat_last AS
WITH last_dates AS
( SELECT cs_country_iso2 AS country,
        MAX(cs_stats_timestamp) AS last_date
    FROM data.country_stat
   WHERE cs_stats_resolution='1d'
   GROUP BY cs_country_iso2
)
SELECT country.c_name, country_stat.*
  FROM data.country_stat
  JOIN last_dates ON (last_date=cs_stats_timestamp AND country=cs_country_iso2)
  JOIN data.country ON c_iso2 = cs_country_iso2
 WHERE cs_stats_resolution='1d';

CREATE OR REPLACE VIEW data.v_asn_neighbour
AS
SELECT an_date,
       an_asn,
       a1.a_country_iso2 as asn_country,
       an_neighbour,
       a2.a_country_iso2 as neighbour_country,
       CASE WHEN a1.a_country_iso2 <> a2.a_country_iso2 THEN TRUE ELSE FALSE END as is_foreign_neighbour,
       an_type,
       an_power,
       an_v4_peers,
       an_v6_peers
  FROM data.asn_neighbour as n
  LEFT JOIN data.asn as a1 ON a1.a_ripe_id = n.an_asn
  LEFT JOIN data.asn as a2 ON a2.a_ripe_id = n.an_neighbour
 WHERE an_type in ('left', 'right');


CREATE OR REPLACE VIEW data.v_connectivity_index_by_country
AS
SELECT asn_country,
       SUM( CASE WHEN is_foreign_neighbour THEN 1 ELSE 0 END ) AS foreign_neighbour_count,
       SUM( CASE WHEN NOT is_foreign_neighbour THEN 1 ELSE 0 END ) AS local_neighbour_count,
       COUNT(*) AS total_neighbour_count,
       sum( CASE WHEN is_foreign_neighbour THEN 1 ELSE 0 END ) :: FLOAT / count(*) AS foreign_neighbours_share
  FROM data.v_asn_neighbour
 WHERE asn_country IS NOT NULL
 GROUP BY asn_country;

CREATE OR REPLACE VIEW data.v_neighbours_by_country
AS
SELECT asn_country,
       neighbour_country,
       count(*) AS neighbours_count
  FROM data.v_asn_neighbour
 GROUP BY asn_country,
          neighbour_country
 ORDER BY asn_country, count(*) DESC;

CREATE OR REPLACE VIEW data.v_connectivity_index_by_asn
AS
SELECT an_asn,
       asn_country,
       SUM( CASE WHEN is_foreign_neighbour THEN 1 ELSE 0 END ) AS foreign_neighbour_count,
       SUM( CASE WHEN NOT is_foreign_neighbour THEN 1 ELSE 0 END ) AS local_neighbour_count,
       COUNT(*) AS total_neighbour_count,
       sum( CASE WHEN is_foreign_neighbour THEN 1 ELSE 0 END ) :: FLOAT / count(*) AS foreign_neighbours_share
  FROM data.v_asn_neighbour
 WHERE asn_country IS NOT NULL
 GROUP BY an_asn, asn_country;