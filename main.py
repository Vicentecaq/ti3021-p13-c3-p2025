"""
CRUD
---
Create: Crear un nuevo registro
Read: Leer registro/s
Update: Actualizar registro
Delete: Borrar registros
---
"""
"""
        pass*
    Palabra reservada para que Ptython no exija el codigo minimo
    necesario para el funcionamiento de la funcion/metodo

        IDE*
    Viene de la palabra Integrated Development Enviroment
    que significa Entorno de desarrollo integrado, que son
    los editores de codigo que normalemnte utilizamos para
    programar en la informatica.

        lint o linter*
    Es el encargado de vigilar que la sintaxis del
    codigo en el IDE sea correcta y te sugiere el
    funcionamiento de este.
"""
# Primero, debemos de crear una clase
class Usuario:
    #Definir cómo se inicializa
    def __init__(self, rut: int, digito_verificador: str, nombres: str, apellidos: str, fecha_nacimiento: date, cod_area: int, telefono: int):

        self.rut: int = rut
        self.digito_verificador: str = digito_verificador
        self.nombres: str = nombres
        self.apellidos: str = apellidos
        self.fecha_nacimiento: date = fecha_nacimiento
        self.cod_area: int = cod_area
        self.telefono: int = telefono

# Creamos una lista para almacenar varios objetos intanciados de la clase Persona
personas: list[Persona] = []

def persona_existente(nueva_persona: Persona) -> bool:
    for persona in personas:
        if persona.rut == nueva_persona.rut:
            print(f"Persona ya existe con rut: {persona.rut}-{persona.digito_verificador}")
            return False
    print("Persona no exiastente.")
    return False

def create_persona():
    rut: int = int(input("Ingrese rut sin digito verificador: "))
    digito_verificador: str = input("Ingrese digito verificador: ")
    nombres: str = input("Ingrese nombres de la persona: ")
    apellidos: str = input("Ingrese apellidos de la persona: ")
    dia_nacimiento: int = int(input("Ingrese el dia de nacimiento: "))
    mes_nacimiento: int = int(input("Ingrese el mes de nacimiento: "))
    anio_nacimiento: int = int(input("Ingrese el año de nacimiento: "))
    fecha_nacimiento: date = date(year=anio_nacimiento, month=mes_nacimiento, day=dia_nacimiento)
    cod_area = input("Ingrese codigo del area del numero de telefono: ")
    telefono = input("Ingrese numero de telefono sin codigo de area: ")
def read_persona():
    pass
def update_persona():
    pass
def delete_persona():
    pass
