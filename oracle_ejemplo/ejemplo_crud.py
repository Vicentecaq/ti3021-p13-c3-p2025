from datetime import datetime
import oracledb
import os
from dotenv import load_dotenv
from typing import Optional

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

def create_all_tables():
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
def update_participantes(
        id: int,
        nombre: Optional[str] = None,
        edad: Optional[int] = None,
        numInscripcion: Optional[int] = None
):
    modificaciones = []
    parametros = {"id": id}

    if nombre is not None:
        modificaciones.append("nombre =: nombre")
        parametros["nombre"] = nombre
    if edad is not None:
        modificaciones.append("edad =: edad")
        parametros["edad"] = edad
    if numInscripcion is not None:
        modificaciones.append("numInscripcion =: numInscripcion")
        parametros["numInscripcion"] = numInscripcion
    if not modificaciones:
        return print("No has enviado datos por modificar")
    
    sql = f"UPDATE PARTICIPANTES SET {", ".join(modificaciones)} WHERE id =: id"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
    conn.commit()
    print(f"Dato con ID={id} actualizado.")

def update_atleta(
        id: int,
        disciplina: str,
        marca: float
):
    modificaciones = []
    parametros = {"id": id}

    if disciplina is not None:
        modificaciones.append("disciplina =: disciplina")
        parametros["disciplina"] = disciplina
    if marca is not None:
        modificaciones.append("marca =: marca")
        parametros["marca"] = marca
        
    sql = f"UPDATE PARTICIPANTES SET {", ".join(modificaciones) } WHERE id =: id"    
    with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
    conn.commit()
    print(f"Dato con ID={id} actualizado.")

def update_juez(
        idParticipantes: int,
        especialidad: str,

):
    modificaciones = []
    parametros = {"id": id}

    if idParticipantes is not None:
        modificaciones.append("idParticipantes =: idParticipantes")
        parametros["idParticipantes"] = idParticipantes
    if especialidad is not None:
        modificaciones.append("especialidad =: especialidad")
        parametros["especialidad"] = especialidad
        
    sql = f"UPDATE JUEZ SET {", ".join(modificaciones) } WHERE id =: id"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, parametros)
    conn.commit()
    print(f"Dato con ID={id} actualizado.")

def update_entrenador(
        idParticipantes: int,
        equipo: str

):
    modificaciones = []
    parametros = {"id": id}

    if idParticipantes is not None:
        modificaciones.append("idParticipantes =: idParticipantes")
        parametros["idParticipantes"] = idParticipantes
    if equipo is not None:
        modificaciones.append("equipo =: equipo")
        parametros["equipo"] = equipo
   
        sql = f"UPDATE JUEZ SET {", ".join(modificaciones) } WHERE id =: id"
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
    conn.commit()
    print(f"Dato con ID={id} actualizado.")

# DELETE - eliminacion de datos
def delete_participantes(id: int):
    sql = (
        "DELETE FROM PARTICIPANTES WHERE id =: id"
    )
    parametros = {"id" : id}
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Dato eliminado \n {parametros}")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al eliminar dato: {err} \n {sql} \n {parametros}")

def delete_atleta(id: int):
    sql = (
        "DELETE FROM ATLETA WHERE id =: id"
    )
    parametros = {"id" : id}
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Dato eliminado \n {parametros}")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al eliminar dato: {err} \n {sql} \n {parametros}")

def delete_juez(id: int):
    sql = (
        "DELETE FROM JUEZ WHERE id =: id"
    )
    parametros = {"id" : id}
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Dato eliminado \n {parametros}")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al eliminar dato: {err} \n {sql} \n {parametros}")

def delete_entrenador(id: int):
    sql = (
        "DELETE FROM ENTRENADOR WHERE id =: id"
    )
    parametros = {"id" : id}
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, parametros)
            conn.commit()
            print(f"Dato eliminado \n {parametros}")
    except oracledb.DatabaseError as e:
        err = e
        print(f"Error al eliminar dato: {err} \n {sql} \n {parametros}")

def main():
    pass

if __name__ == "__main__":
    main()