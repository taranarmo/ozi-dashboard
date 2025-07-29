\connect ozi_db2
CREATE OR REPLACE VIEW data.v_asn_neighbour
AS
SELECT an_date,
       an_asn,
       a1.asn_country,
       an_neighbour,
       a2.asn_country as neighbour_country,
       CASE WHEN a1.asn_country <> a2.asn_country THEN TRUE ELSE FALSE END as is_foreign_neighbour,
       an_type,
       an_power,
       an_v4_peers,
       an_v6_peers
  FROM data.asn_neighbour as n
   JOIN data.v_current_asn as a1 ON (a1.asn_id = n.an_asn)
   JOIN data.v_current_asn as a2 ON (a2.asn_id = n.an_neighbour)
 WHERE an_type in ('left', 'right');


GRANT SELECT ON data.v_connectivity_index_by_country TO looker_user;
