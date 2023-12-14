DROP TABLE IF EXISTS public.aeropuertos;

DROP TABLE IF EXISTS public.metarreports;

CREATE TABLE Aeropuertos (
    codigo_aeropuerto VARCHAR(6) PRIMARY KEY,
    nombre VARCHAR(255),
	latitude FLOAT,
	longitude FLOAT,
	elevation FLOAT
);

CREATE TABLE MetarReports (
    id_reporte SERIAL PRIMARY KEY,
    codigo_aeropuerto VARCHAR(4) REFERENCES Aeropuertos(codigo_aeropuerto),
    fecha_hora TIMESTAMP,
    datos_metar TEXT,
	dia_metar TEXT,
	hora_metar TEXT,
    viento_dir INTEGER,
    viento_int INTEGER,
    visibilidad FLOAT,
	fen_obst TEXT,
    techo1 TEXT,
    techo2 TEXT,
    techo3 TEXT,
	alttech1 INTEGER,
	alttech2 INTEGER,
	alttech3 INTEGER,
    temperatura FLOAT,
    pto_rocio FLOAT,
    altimetro FLOAT,
    nubosidad1 INTEGER,
    nubosidad2 INTEGER,
    nubosidad3 INTEGER,
    rmk TEXT
);