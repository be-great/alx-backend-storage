-- select by order
SELECT band_name, IFNULL(2022 - formed, 2022) AS lifespan 
FROM metal_bands 
WHERE style = 'Glam rock' 
ORDER BY lifespan DESC;
