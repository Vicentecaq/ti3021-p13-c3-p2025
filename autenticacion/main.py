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
                "id_u INTEGER PRIMARY KEY,"
                "username VARCHAR(32) UNIQUE,"
                "password RAW(200)"
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

    def query(self, sql: str, parameters: Optional[dict] = None):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, parameters or {})
                    if sql.strip().upper().startswith("SELECT"):
                        return cur.fetchall()
                conn.commit()
                return True
        except oracledb.DatabaseError as error:
            print(f"\n[Error Oracle]: {error}")
            return None

class Auth: 
    @staticmethod
    def register(db: Database, id_u: int, username: str, password: str):
        print("registrando usuario")
        password_bytes = password.encode("UTF-8")
        salt = bcrypt.gensalt(12)
        hash_password = bcrypt.hashpw(password_bytes,salt)

        usuario = {
            "id_v": id_u,
            "user_v": username,
            "pw_v": hash_password
        }

        sql_insert = "INSERT INTO USERS(id_u,username,password) VALUES (:id_v, :user_v, :pw_v)"
        resultado = db.query(sql=sql_insert, parameters=usuario)
        
        if resultado:
            print("usuario registrado con exito")
        else:
            print("No se pudo registrar el usuario.")

    @staticmethod
    def login(db: Database, username: str, password: str) -> bool:
#       password_enc = password.encode("UTF-8")
        sql_login = "SELECT password FROM USERS WHERE username = :u"
        resultado = db.query(sql = sql_login, parameters={"u": username})
        
        if not resultado:
            print("\nUsuario no existe.")
            return False

        # hashed_password = resultado[0][0]
        hash_en_db = resultado[0][0]

        try:
            if bcrypt.checkpw(password.encode("UTF-8"), hash_en_db):
                print("\nLogeado correctamente.")
                return True
            else:
                print("\nContraseña incorrecta.")
                return False
        except Exception as e:
            print(f"Error al verificar contraseña: {e}")
            return False

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

            if "serie" in respuesta and len(respuesta["serie"]) > 0:
                return respuesta["serie"][0]["valor"]
            return None
        except Exception as e:
            print(f"Hubo un error con la solicitud: {e}")
            return None

    def save_indicator(self, db, indicator, value, username):
        sql = """
            INSERT INTO indicator_log
            (indicator_name, indicator_value, query_date, username, source)
            VALUES
            (:i_name, :v_value, SYSDATE, :u_user, :s_src)
        """
        params = {
            "i_name": indicator.upper(),
            "v_value": value,
            "u_user": username,
            "s_src": "https://mindicador.cl"
        }
        resultado = db.query(sql, params)

        if resultado:
            ("[DB] Datos guardados en el historial correctamente.")
        else:
            print("[!] Error: Los datos no se pudieron guardar en la base de datos.")
        
    def get_usd(self, db, user, fecha: str = None):
        valor = self.get_indicator("dolar", fecha)
        if valor:
            print(f"\n[API] El valor del dólar es: ${valor}")
            self.save_indicator(db, "dolar", valor, user)
            print("[DB] Guardado en el historial.")
        else:
            print("\n[!] No se pudo obtener el valor del dólar.")
    def get_eur(self, db, user, fecha: str = None):
        valor = self.get_indicator("euro", fecha)
        if valor:
            print(f"\n[API] El valor del EURO es: ${valor}")
            self.save_indicator(db, "euro", valor, user)
            print("[DB] Guardado en el historial.")
    def get_uf(self, db, user, fecha: str = None):
        valor = self.get_indicator("uf", fecha)
        if valor:
            print(f"\n[API] El valor de la UF es: ${valor}")
            self.save_indicator(db, "uf", valor, user)
            print("[DB] Guardado en el historial.")
    def get_ivp(self, db, user, fecha: str = None):
        valor = self.get_indicator("ivp", fecha)
        if valor:
            print(f"\n[API] El valor del IVP es: ${valor}")
            self.save_indicator(db, "ivp", valor, user)
            print("[DB] Guardado en el historial.")     
    def get_ipc(self, db, user, fecha: str = None):
        valor = self.get_indicator("ipc", fecha)
        if valor:
            print(f"\n[API] El valor del IPC es: {valor}%")
            self.save_indicator(db, "ipc", valor, user)
            print("[DB] Guardado en el historial.")
    def get_utm(self, db, user, fecha: str = None):
        valor = self.get_indicator("utm", fecha)
        if valor:
            print(f"\n[API] El valor de la UTM es: ${valor}")
            self.save_indicator(db, "utm", valor, user)
            print("[DB] Guardado en el historial.")    
 
if __name__ == "__main__":
    db = Database(
        username=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"), 
        dsn=os.getenv("ORACLE_DSN")
        )
    fin = Finance()
    db.create_all_tables()

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== SISTEMA DE INDICADORES ===")
        print("1. Iniciar Sesión\n2. Registrarse\n0. Salir")
        opc = input("Seleccione: ")

        if opc == "1":
            u = input("Usuario: ").strip()
            p = input("Contraseña: ").strip()
            
            if Auth.login(db, u, p):
                input("Presione ENTER para ir al Menu de Consultas...")

                while True:
                    os.system("cls" if os.name == "nt" else "clear")
                    print(f"USUARIO ACTIVO: {u.upper()}")
                    print("-" * 25)
                    print("1. Dolar\n2. Euro\n3. UF\n4. IVP\n5. IPC\n6. UTM\n0. Cerrar Sesión")
                    sub = input("Opción: ")

                    if sub == "1":
                        fin.get_usd(db, u)
                    elif sub == "2":
                        fin.get_eur(db, u)
                    elif sub == "3":
                        fin.get_uf(db, u)
                    elif sub == "4":
                        fin.get_ivp(db, u)
                    elif sub == "5":
                        fin.get_ipc(db, u)
                    elif sub == "6":
                        fin.get_utm(db, u)
                    elif sub == "0": 
                        break
    
                    input("\nPresione ENTER para continuar...")
            else:
                input("\nPresione ENTER para reintentar...")
        
        elif opc == "2":
            try:
                id_reg = int(input("ID para el usuario: "))
                user_reg = input("Nombre de usuario: ")
                pass_reg = input("Contraseña: ")
                Auth.register(db, id_reg, user_reg, pass_reg)
            except ValueError:
                print("Error: El ID debe ser un número entero.")
            input("\nENTER para volver...")
            
        elif opc == "0": 
            print("Cerrando programa...")
            break