--SELECT g.name, gw.date_worn FROM garment g JOIN garment_wears gw ON g.garment_id=gw.garment_id ORDER BY gw.date_worn;

-- wears since last wash
SELECT g.name,  e.date_worn, e.date_washed, MIN(e.date_worn), MAX(e.date_worn), MAX(e.date_washed) AS last_wash,
-- CAST (julianday(date('now')) - julianday(date(e.date_washed)) AS INTEGER) AS wears_since_last_wash 
COUNT(e.date_worn) AS wears_since_last_wash 
FROM garment g JOIN events e ON g.garment_id=e.garment_id
WHERE e.date_worn > g.last_washed OR g.last_washed IS NULL -- (SELECT DATE('now')) --(SELECT MAX(e.date_washed) FROM events e )
GROUP BY g.garment_id
HAVING COUNT(e.date_worn) > 1;