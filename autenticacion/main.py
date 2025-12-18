# Conectarnos a la base de datos
import oracledb
import requests
# Rescatar variables de entorno
import os
from dotenv import load_dotenv
import bcrypt
# Importar el tipo de dato opcional
from typing import Optional
import datetime

load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

class Database:
    def __init__(self,username,password,dsn):
        self.username = username
        self.dsn = dsn
        self.password = password

    def get_connection(self):
        return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)
    
    def create_all_tables(self):
        tables = [
            "CREATE TABLE USERS("
                "id INTEGER PRIMARY KEY,"
                "username VARCHAR(32) UNIQUE,"
                "password VARCHAR(128)"
            ")",
            "CREATE TABLE indicator_log("
                "id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,"
                "indicator_name VARCHAR(20),"
                "indicator_value NUMBER,"
                "indicator_date DATE,"
                "query_date DATE,"
                "username VARCHAR(50),"
                "source VARCHAR(100)"
            ")"
        ]

        for table in tables:
            try:
                self.query(table)
            except:
                pass

    def query(self, sql: str, parameters: Optional [dict] = None):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    ejecucion = cur.execute(sql, parameters)
                    if sql.startswith("SELECT"):
                        resultado = []
                        for fila in ejecucion:
                            resultado.append(fila)
                        return resultado
                conn.commit()
        except oracledb.DatabaseError as error:
            print(error)

class Auth: 
    @staticmethod
    def register(db: Database, id: int, username: str, password: str):
        print("registrando usuario")
        password = password.encode("UTF-8")
        salt = bcrypt.gensalt(12)
        hash_password = bcrypt.hashpw(password,salt)

        usuario = {
            "id": id,
            "username": username,
            "password": hash_password
        }

        db.query(
            sql= "INSERT INTO USERS(id,username,password) VALUES (:id, :username, :password)",
            parameters=usuario
        )
        print("usuario registrado con exito")

    @staticmethod
    def login(db: Database, username: str, password: str):
        password = password.encode("UTF-8")

        resultado = db.query(
            sql= "SELECT * FROM USERS WHERE username = :username",
            parameters={"username":username}
        )

        if len(resultado) == 0:
            return print("No hay coincidencias")
        
        hashed_password = bytes.fromhex(resultado[0][2])

        if bcrypt.checkpw(password, hashed_password):
            return print("Logeado correctamente")
        else:
            return print("Contraseña incorrecta")

class Finance:
    def __init__(self, base_url: str = "https://mindicador.cl/api"):
        self.base_url = base_url
    def get_indicator(self, indicator: str, fecha: str = None) -> float:
        try:
            if not fecha:
                dd = datetime.datetime.now().day
                mm = datetime.datetime.now().month
                yyyy = datetime.datetime.now().year
                fecha = f"{dd}-{mm}-{yyyy}"
            url = f"{self.base_url}/{indicator}/{fecha}"
            respuesta = requests.get(url).json()
            return respuesta["serie"][0]["valor"]
        except:
            print("Hubo un error con la solicitud")
    def get_usd(self, fecha: str = None):
        valor = self.get_indicator("dolar", fecha)
        print(f"El valor del dolar en CLP es: {valor}")
    def get_eur(self, fecha: str = None):
        self.get_indicator("euro", fecha)
    def get_uf(self, fecha: str = None):
        self.get_indicator("uf", fecha)
    def get_ivp(self, fecha: str = None):
        self.get_indicator("ivp", fecha)
    def get_ipc(self, fecha: str = None):
        self.get_indicator("ipc", fecha)
    def get_utm(self, fecha: str = None):
        self.get_indicator("utm", fecha)

def menu_principal():
    print(
        """
            ====================================
            |         Menu Principal           |
            |----------------------------------|
            | 1. Iniciar sesion                |
            | 2. Salir                         |
            ====================================
        """
    )

def menu_indicadores():
    print(
        """
            ====================================
            |           Indicadores            |
            |----------------------------------|
            | 1. UF                            |
            | 2. Dolar                         |
            | 3. Euro                          |
            | 4. IVP                           |
            | 5. IPC                           |
            | 6. UTM                           |
            | 7. Volver                        |
            ====================================
        """
    )

if __name__ == "__main__":
    db= Database(
        username=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN")
        )
    Finance = Finance()

    while True:
        menu_principal()
        opcion = input("Seleccione una opcion: ")
        
        if opcion == "1":
            usuario = input("Usuario: ")
            password = input("Contraseña: ")

            if Auth.login(db, usuario, password):
                print("Bienvenido", usuario)

                while True:
                    menu_indicadores()
                    op = input("Seleccione indicador: ")

                    if op == "1":
                        Finance.get_uf(db, usuario)
                    elif op == "2":
                        Finance.get_usd(db, usuario)
                    elif op == "3":
                        Finance.get_eur(db, usuario)
                    elif op == "4":
                        Finance.get_ivp(db, usuario)
                    elif op == "5":
                        Finance.get_ipc(db, usuario)
                    elif op == "6":
                        Finance.get_utm(db, usuario)
                    elif op == "7":
                        break
                    else:
                        print("Opción no válida")
            else:
                print("Usuario o contraseña incorrectos")

        elif opcion == "2":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    db= Database(
        username=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN")
        )
    Finance = Finance()
    db.create_all_tables()
    db.query("SELECT * FROM USERS")

    Auth.login(db,"soyelseba","alskjflsakf")