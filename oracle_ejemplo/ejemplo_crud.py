from datetime import datetime
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
        "CREATE TABLE PARTICIPANTES ("
        "id INTEGER PRIMARY KEY,"
        "nombre VARCHAR(64),"
        "edad INTEGER,"
        "numInscripcion INTEGER,"
        ")"
    ),
    (
        "CREATE TABLE ATLETA("
        "id INTEGER PRIMARY KEY,"
        "disciplina VARCHAR(64),"
        "marca FLOAT,"
        "FOREIGN KEY (idParticipante) REFERENCES PARTICIPANTES(id)"
        ")"
    ),
    (
        "CREATE TABLE JUEZ ("
        "idParticipante INTEGER PRIMARY KEY,"
        "especialidad VARCHAR2(64),"
        "FOREIGN KEY (idParticipante) REFERENCES PARTICIPANTES(id)"
        ")"
    ),
    (
        "CREATE TABLE ENTRENADOR ("
        "idParticipante INTEGER PRIMARY KEY,"
        "equipo VARCHAR2(64),"
        "FOREIGN KEY (idParticipante) REFERENCES PARTICIPANTES(id)"
        ")"
    ),
]

for query in tables:
    create_schema(query)

# CREATE - insercion de datos
def create_participante(
    id: int,
    nombre: str,
    edad: int,
    numInscripcion: int
):
    sql = (
    "INSERT INTO participantes(id, nombre, edad, numInscripcion) "
    "VALUES (:id, :nombre, :edad, :numInscripcion)"
    )

    parametros = {
    "id": id,
    "nombre": nombre,
    "edad": edad,
    "numInscripcion": numInscripcion
    #"fecha_nacimiento": datetime.strptime(fecha_nacimiento, '%d-%m-%Y')
    }

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
            connection.commit()
            print("Inserción de participante correcta")
    except oracledb.DatabaseError as error:
        print(f"No se pudo insertar el participante \n {error} \n {sql} \n {parametros}")   
        
def create_atleta(
    idParticipante,
    disciplina,
    marca
):
    
    sql = (
        "INSERT INTO ATLETA(idParticipante, disciplina, marca) "
        "VALUES (:idParticipante, :disciplina, :marca)"
    )

    parametros = {
        "idParticipante": idParticipante,
        "disciplina": disciplina,
        "marca": marca
    }

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
            connection.commit()
            print("Inserción de atleta correcta")
    except oracledb.DatabaseError as error:
        print(f"No se pudo insertar el atleta \n {error} \n {sql} \n {parametros}")

def create_juez(
    idParticipante,
    especialidad
    ):
    
    sql = (
        "INSERT INTO JUEZ(idParticipante, especialidad) "
        "VALUES (:idParticipante, :especialidad)"
    )

    parametros = {
        "idParticipante": idParticipante,
        "especialidad": especialidad
    }

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
            connection.commit()
            print("Inserción de juez correcta")
    except oracledb.DatabaseError as error:
        print(f"No se pudo insertar el juez \n {error} \n {sql} \n {parametros}")

def create_entrenador(
    idParticipante,
    equipo
    ):
    
    sql = (
        "INSERT INTO ENTRENADOR(idParticipante, equipo) "
        "VALUES (:idParticipante, :equipo)"
    )

    parametros = {
        "idParticipante": idParticipante,
        "equipo": equipo
    }

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, parametros)
            connection.commit()
            print("Inserción de entrenador correcta")
    except oracledb.DatabaseError as error:
        print(f"No se pudo insertar el entrenador \n {error} \n {sql} \n {parametros}")

# READ - Lectura de datos

def read_participantes():
    sql = (
        "SELECT * FROM PARTICIPANTES"
        )
    
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql)
                resultados = cursor.execute(sql)
                for fila in resultados:
                    print(fila)
    except oracledb.DatabaseError as error:
        print(f"No se pudo ejecutar la query {error}\n{sql}")

def read_participante_by_id(id: int):
    sql = (
        "SELECT * FROM PARTICIPANTES WHERE id = :id"
    )
    parametros = {"id": id}

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql, parametros)
                resultados = cursor.execute(sql, parametros)
                filas = list(resultados)
                if len(filas) == 0:
                    return print(f"No hay registros con el ID {id}")
                for fila in filas:
                    print(fila)
    except oracledb.DatabaseError as error:
        print(f"No se pudo ejecutar la query {error} \n {sql} \n {parametros}")

def read_atletas():
    sql = (
        "SELECT * FROM ATLETA"
        )
    
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql)
                resultados = cursor.execute(sql)
                for fila in resultados:
                    print(fila)
    except oracledb.DatabaseError as error:
        print(f"No se pudo ejecutar la query {error}\n{sql}")

def read_atleta_by_id(id: int):
    sql = (
        "SELECT * FROM ATLETA WHERE id = :id"
    )
    parametros = {"id": id}

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql, parametros)
                resultados = cursor.execute(sql, parametros)
                filas = list(resultados)
                if len(filas) == 0:
                    return print(f"No hay registros con el ID {id}")
                for fila in filas:
                    print(fila)
    except oracledb.DatabaseError as error:
        print(f"No se pudo ejecutar la query {error} \n {sql} \n {parametros}")

def read_jueces():
    sql = (
        "SELECT * FROM JUEZ"
        )
    
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql)
                resultados = cursor.execute(sql)
                for fila in resultados:
                    print(fila)
    except oracledb.DatabaseError as error:
        print(f"No se pudo ejecutar la query {error}\n{sql}")

def read_juez_by_id(id: int):
    sql = (
        "SELECT * FROM JUEZ WHERE id = :id"
    )
    parametros = {"id" : id}

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql, parametros)
                resultados = cursor.execute(sql, parametros)
                filas = list(resultados)
                if len(filas) == 0:
                    return print(f"No hay registros con el ID {id}")
                for fila in filas:
                    print(fila)
    except oracledb.DatabaseError as error:
        print(f"No se pudo ejecutar la query {error} \n {sql} \n {parametros}")


def read_entrenadores():
    sql = (
        "SELECT * FROM ENTRENADOR"
        )
    
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql)
                resultados = cursor.execute(sql)
                for fila in resultados:
                    print(fila)
    except oracledb.DatabaseError as error:
        print(f"No se pudo ejecutar la query {error}\n{sql}")

def read_entrenador_by_id(id: int):
    sql = (
        "SELECT * FROM ENTRENADOR WHERE id = :id"
    )
    parametros = {"id": id}

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                print(sql, parametros)
                resultados = cursor.execute(sql, parametros)
                filas = list(resultados)
                if len(filas) == 0:
                    return print(f"No hay registros con el ID {id}")
                for fila in filas:
                    print(fila)
    except oracledb.DatabaseError as error:
        print(f"No se pudo ejecutar la query {error} \n {sql} \n {parametros}")

# UPDATE - Actualización de datos