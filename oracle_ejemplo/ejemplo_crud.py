import oracledb
import os
from dotenv import load_dotenv
load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

def get_connection():
    return oracledb.connect(user=username, password=password, dsn=dsn)

def create_schema(query):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                print(f"Tabla creada \n {query}")
    except oracledb.DatabaseError as error:
        print(f"No se pudo crear la tabla: {error}")

tables = [
    (
        "CREATE TABLE PERSONAS ("
        "id INTEGER PRIMARY KEY,"
        "rut VARCHAR(8),"
        "nombres VARCHAR(64),"
        "apellidos VARCHAR(64),"
        "fecha_nacimiento DATE"
        ")"
    ),
    (
        "CREATE TABLE DEPARTAMENTO("
        "id INTEGER PRIMARY KEY,"
        "nombre VARCHAR(32),"
        "fecha_creacion DATE"
        ")"
    ),
    (
        "CREATE TABLE EMPLEADO ("
        "id INTEGER PRIMARY KEY,"
        "sueldo INTEGER,"
        "idPersona INTEGER NOT NULL,"
        "idDepartamento INTEGER NOT NULL,"
        "FOREIGN KEY (idPersona) REFERENCES PERSONAS(id),"
        "FOREIGN KEY (idDepartamento) REFERENCES DEPARTAMENTO(id)"
        ")"
    )
]

# for query in tables:
#     create_schema(query)


from datetime import datetime
def create_persona(id: int, rut: str, nombres: str, apellidos: str, fecha_nacimiento: str):
    sql = (
    "INSERT INTO personas (id, rut, nombres, apellidos, fecha_nacimiento) "
    "VALUES (:id, :rut, :nombres, :apellidos, :fecha_nacimiento)"
    )
    bind_fecha = None
    if fecha_nacimiento:
        bind_fecha = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")

        parametros = {
                "id": id,
                "rut": rut,
                "nombres": nombres,
                "apellidos": apellidos,
                "fecha_nacimiento": bind_fecha
                }
        
        print(parametros)

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()

    print(f"Persona con RUT={rut} creada.")

def read_persona(id: int):
    sql = (
        "SELECT * FROM "
    )