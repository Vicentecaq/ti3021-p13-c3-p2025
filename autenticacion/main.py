# Conectarnos a la base de datos
import oracledb
# Rescatar variables de entorno
import os
from dotenv import load_dotenv
import bcrypt
# Importar el tipo de dato opcional
from typing import Optional

load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

class Database:
    def __init__(self,username,password,dsn):
        self.username = username
        self.password = password
        self.dsn = dsn
    def get_connection(self):
        return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)
    def create_all_tables(self):
        pass
    def query(self, sentence: str, parameters: Optional [dict] = None):
        print(f"Ejecutando query:\n{sentence}\nParametros:\n{parameters}")
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    resultado = cursor.execute(sentence, parameters)
                    for fila in resultado:
                        print(fila)
                connection.commit()
        except oracledb.DatabaseError as error:
            print(f"Hubo un error con la base de datos:\n{error}")


class Auth: 
    @staticmethod
    def register():
        pass
    @staticmethod
    def login():
        pass

class Finance:
    @staticmethod
    def get_uf():
        pass
    @staticmethod
    def get_ivp():
        pass
    @staticmethod
    def get_pc():
        pass
    @staticmethod
    def get_utm():
        pass
    @staticmethod
    def get_usd():
        pass
    @staticmethod
    def get_eur():
        pass

if __name__ == "__main__":
    db= Database(username=username, password=password, dsn=dsn)
    db.query("SELECT sysdate FROM dual")