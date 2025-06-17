select date_trunc('week', cs_stats_timestamp)::date,
       round(avg(cs_v4_prefixes_ris)) as avg_cs_v4_prefixes_ris,
       round(avg(cs_v6_prefixes_ris)) as avg_cs_v6_prefixes_ris,
       round(avg(cs_asns_ris)) as avg_cs_asns_ris,
       round(avg(cs_asns_stats)) as avg_cs_asns_stats
from data.country_stat
where cs_country_iso2='RU' and cs_stats_resolution = '1d'
group by date_trunc('week', cs_stats_timestamp)::date
order by date_trunc('week', cs_stats_timestamp)::date;