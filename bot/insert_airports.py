import psycopg2
import json

# Configuración de la conexión a la base de datos
conexion = psycopg2.connect(
    user='dsm',
    password='dsm_services12345',
    host='localhost',
    port='5432',
    database='metars'
)

# Abre un cursor para ejecutar operaciones en la base de datos
cursor = conexion.cursor()

# Ruta al archivo JSON
ruta_json = 'airbases.json'

# Lee los datos desde el archivo JSON
with open(ruta_json, 'r') as archivo_json:
    datos_aeropuertos = json.load(archivo_json)

# Inserta los datos en la base de datos
for aeropuerto in datos_aeropuertos:
    cursor.execute("""
        INSERT INTO aeropuertos (codigo_aeropuerto, nombre, latitude, longitude, elevation)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        aeropuerto['id'],
        aeropuerto['name'],
        aeropuerto['longitude'],
        aeropuerto['latitude'],
        aeropuerto['heigh']
    ))

# Realiza commit para aplicar los cambios
conexion.commit()

# Cierra el cursor y la conexión
cursor.close()
conexion.close()
