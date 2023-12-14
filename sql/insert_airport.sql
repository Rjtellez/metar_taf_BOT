-- Inserta el nuevo aeropuerto en la tabla aeropuertos
INSERT INTO aeropuertos (
  codigo_aeropuerto, 
  nombre, 
  latitude, 
  longitude,
  elevation
) VALUES (
  'MMMTP', -- designador del aeropuerto
  'EMM31', -- nombre del aeropuerto
  14.89,  -- latitud del aeropuerto
  -92.25, -- longitud del aeropuerto
  30 -- elevacion del aeropuerto
);

INSERT INTO aeropuertos (
  codigo_aeropuerto, 
  nombre, 
  latitude, 
  longitude,
  elevation
) VALUES (
  'MMMD', -- designador del aeropuerto
  'MERIDA AIRPORT', -- nombre del aeropuerto
  20.9369,  -- latitud del aeropuerto
  -89.6577, -- longitud del aeropuerto
  38 -- elevacion del aeropuerto
);
select * from aeropuertos
where codigo_aeropuerto = 'MMMMZ';

select * from metarreports
where codigo_aeropuerto = 'MMM27'
order by fecha_hora desc;
