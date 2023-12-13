import os
import psycopg2
from datetime import datetime, timedelta
from dotenv import load_dotenv
from metar_taf_parser.parser.parser import MetarParser

load_dotenv()

class Insert:
    
    def __init__(self):
        pass
    
    def insert_metar(self, report):
        report = report
        # Configuración de la conexión a la base de datos
        conexion = psycopg2.connect(
            user= os.getenv("DB_USER"),
            password= os.getenv("DB_PASSWORD"),
            host= os.getenv("DB_HOST"),
            port= os.getenv("DB_PORT"),
            database= os.getenv("DB_NAME")
        )

        # Abre un cursor para ejecutar operaciones en la base de datos
        cursor = conexion.cursor()

        

        # Inserta los datos en la base de datos
        
        metar = MetarParser().parse(report)
        codigo = metar.station
        fecha_hora = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        report = metar.message
        dia = metar.day
        hora = metar.time.isoformat()
        viento_dir = metar.wind.degrees
        viento_int = metar.wind.speed
        visibilidad = eval(metar.visibility.distance.rstrip("SM").replace(" ", "+").replace(">", "").replace("km", ""))
        fen_obst = [str(x.phenomenons[0])[11:] for x in metar.weather_conditions]

        if len(metar.clouds)> 0:
            techo1 = metar.clouds[0].quantity.name
            alttech1 = metar.clouds[0].height
        else:
            techo1 = None
            alttech1 = None

        if len(metar.clouds) > 1:
            techo2 = metar.clouds[1].quantity.name
            alttech2 = metar.clouds[1].height
        else:
            techo2 = None
            alttech2 = None

        if len(metar.clouds) > 2:
            techo3 = metar.clouds[2].quantity.name
            alttech3 = metar.clouds[2].height

        else:
            techo3 = None
            alttech3 = None
        
        temperatura = metar.temperature
        pto_rocio = metar.dew_point
        altimetro = metar.altimeter

        if len(metar.remarks) > 0:
            rmk = [x for x in metar.remarks if x.startswith('8/')]
            if rmk:
                rmknub = rmk[0][2:]
                if rmknub[0] == "/":
                    nubosidad1 = None
                else:
                    nubosidad1 = rmknub[0]
                if rmknub[1] == "/":
                    nubosidad2 = None
                else:
                    nubosidad2 = rmknub[1]
                if rmknub[2] == "/":
                    nubosidad3 = None
                else:
                    nubosidad3 = rmknub[2]
            else:
                rmknub = None
                nubosidad1 = None
                nubosidad2 = None
                nubosidad3 = None
        else: 
            rmknub = None
            nubosidad1 = None
            nubosidad2 = None
            nubosidad3 = None


        rmk = metar.remark

        cursor.execute("""INSERT INTO metarreports (
                codigo_aeropuerto, 
                fecha_hora, 
                datos_metar, 
                dia_metar,
                hora_metar,
                viento_dir, 
                viento_int, 
                visibilidad,
                fen_obst,
                techo1, 
                techo2,
                techo3,
                alttech1,
                alttech2,
                alttech3,
                temperatura, 
                pto_rocio, 
                altimetro, 
                nubosidad1, 
                nubosidad2, 
                nubosidad3, 
                rmk
                ) VALUES (%s,%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            codigo, #codigo aeropuerto
            fecha_hora, #fecha y hora
            report, #datos metar
            dia,
            hora,
            viento_dir, #viento direccion
            viento_int, #viento intensidad
            visibilidad, #visibilidad
            fen_obst,
            techo1,
            techo2,
            techo3,
            alttech1,
            alttech2,
            alttech3,
            temperatura,
            pto_rocio,
            altimetro,
            nubosidad1,
            nubosidad2,
            nubosidad3,
            rmk
        ))

        # Realiza commit para aplicar los cambios
        conexion.commit()
        print('Su reporte fue correctamente guardado en la base de datos')
        # Cierra el cursor y la conexión
        cursor.close()
        conexion.close()

class Get:

    def __init__(self):
        pass

    def get_last(self, codigo_aeropuerto):
    # Configuración de la conexión a la base de datos
        conexion = psycopg2.connect(
            user= os.getenv("DB_USER"),
            password= os.getenv("DB_PASSWORD"),
            host= os.getenv("DB_HOST"),
            port= os.getenv("DB_PORT"),
            database= os.getenv("DB_NAME")
        )

        # Abre un cursor para ejecutar operaciones en la base de datos
        cursor = conexion.cursor()
        # 
        try:
            # Consulta para obtener el último reporte para un aeropuerto específico
            consulta = """
                SELECT datos_metar FROM metarreports
                WHERE codigo_aeropuerto = %s
                ORDER BY fecha_hora DESC
                LIMIT 1;
            """
            cursor.execute(consulta, (codigo_aeropuerto,))
            
            # Obtén el resultado
            resultado = cursor.fetchone()

            if resultado:
                # Si se encuentra un resultado, imprímelo o procesa según tus necesidades
                print("Último reporte para el aeropuerto {}: {}".format(codigo_aeropuerto, resultado))
                return resultado
            else:
                print("No se encontraron reportes para el aeropuerto {}".format(codigo_aeropuerto))

        except Exception as e:
            print("Error al ejecutar la consulta:", e)

        finally:
            # Cierra el cursor y la conexión
            cursor.close()
            conexion.close()

