-- Inserta el reporte METAR en la tabla ReportesMETAR
INSERT INTO metarreports (
  codigo_aeropuerto, 
  fecha_hora, 
  datos_metar, 
  dia_metar,
  hora_metar,
  viento_dir, 
  viento_int, 
  visibilidad, 
  techo1, 
  techo2,
  alttech1,
  alttech2,
  temperatura, 
  pto_rocio, 
  altimetro, 
  nubosidad1, 
  nubosidad2, 
  nubosidad3, 
  rmk
) VALUES (
  'MMMX', 
  NOW(), 
  'MMMX 292037Z 29010KT 7SM -TSRA BKN020CB BKN080 18/11 A3026 NOSIG RMK 8/960 HZY TSB35 RAB35', 
  290, 
  10, 
  7, 
  3, 
  2, 
  2000,
  8000,
  18.0, 
  11.0, 
  30.26, 
  9, 
  6, 
  0, 
  'HZY TSB35 RAB35'
);
