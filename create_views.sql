
CREATE VIEW data.v_asn_neighbour
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


 select asn_country,
       sum( case when is_foreign_neighbour then 1 else 0 end ) as foreign_neighbour_count,
       sum( case when NOT is_foreign_neighbour then 1 else 0 end ) as local_neighbour_count,
       count(*) as total_neighbour_count,
       sum( case when is_foreign_neighbour then 1 else 0 end ) :: FLOAT / count(*) as foreign_neighbours_share
  from data.v_asn_neighbour
 where asn_country IS NOT NULL
 group by 1

 select asn_country, neighbour_country, count(*)
from data.v_asn_neighbour
group by 1,2
order by 1, 3 desc
