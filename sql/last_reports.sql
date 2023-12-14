-- Consultar ultimos reportes
WITH last_reports AS(
WITH last_metars AS (
    SELECT
        m.codigo_aeropuerto,
        m.fecha_hora,
        m.datos_metar,
        ROW_NUMBER() OVER (PARTITION BY m.codigo_aeropuerto ORDER BY m.fecha_hora DESC) AS row_num
    FROM
        metarreports m
    WHERE
        COALESCE(LENGTH(m.codigo_aeropuerto) >= 5, FALSE)
        AND (m.fecha_hora IS NULL OR m.fecha_hora >= CURRENT_TIMESTAMP AT TIME ZONE 'UTC' - INTERVAL '1 hour 10 minutes')
)
SELECT 
    a.codigo_aeropuerto,
    COALESCE(m.fecha_hora, CURRENT_TIMESTAMP AT TIME ZONE 'UTC' - INTERVAL '1 hour 10 minutes') AS fecha_hora,
    m.datos_metar
FROM 
    aeropuertos a
LEFT JOIN 
    last_metars m ON a.codigo_aeropuerto = m.codigo_aeropuerto
WHERE
    (m.row_num = 1 AND COALESCE(LENGTH(a.codigo_aeropuerto) >= 5, FALSE))
    OR (m.row_num IS NULL AND COALESCE(m.fecha_hora, CURRENT_TIMESTAMP AT TIME ZONE 'UTC' - INTERVAL '1 hour 10 minutes') >= CURRENT_TIMESTAMP AT TIME ZONE 'UTC' - INTERVAL '1 hour 10 minutes')
)
SELECT * FROM last_reports
WHERE LENGTH(codigo_aeropuerto) >=5
;