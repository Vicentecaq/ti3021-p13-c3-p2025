import oracledb
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")

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

class Database:
    def __init__(self,username,password,dsn):
        self.username = username
        self.password = password
        self.dsn = dsn
    def get_connection(self):
        return oracledb.connect(user=self.username, password=self.password, dsn=self.dsn)