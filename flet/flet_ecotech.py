from ecotech import Auth, Database, Finance
from dotenv import load_dotenv
import flet as ft 
import os

load_dotenv(dotenv_path="flet/.env")

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Ecotech Solutions"

        self.page.bgcolor = "#f2f4f7"
        self.page.padding = 30
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER

        self.db = Database(
            username=os.getenv("ORACLE_USER"),
            password=os.getenv("ORACLE_PASSWORD"),
            dsn=os.getenv("ORACLE_DSN")
        )

        try:
            self.db.create_all_tables()
        except Exception:
            pass

        self.loged_user = ""
        self.page_register()

    def page_register(self):
        self.page.controls.clear()
        
        self.input_id = ft.TextField(
            label="ID del usuario",
            hint_text="Ingresa un número para el ID del usuario"
        )
        self.input_username = ft.TextField(
            label="Nombre de usuario",
            hint_text="Ingresa un nombre de usuario"
        )
        self.input_password = ft.TextField(
            label="Contraseña",
            hint_text="Ingresa una contraseña",
            password=True,
            can_reveal_password=True
        )
        self.button_register = ft.ElevatedButton(
            "Registrarse",
            on_click=self.handle_register
        )
        self.text_status = ft.Text(
            value="", color="red"
        )

        self.button_go_login = ft.TextButton(
        "¿Ya tienes cuenta? Inicia sesión",
        on_click=lambda _: self.page_login()
        )

        card = ft.Container(
            width=400,
            padding=25,
            bgcolor="white",
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=10, color="black12"),
            content=ft.Column(
                spacing=15,
                controls=[
                    ft.Text("Registro", size=22, weight=ft.FontWeight.BOLD),
                    self.input_id,
                    self.input_username,
                    self.input_password,
                    self.button_register,
                    self.text_status,
                    ft.Divider(),
                    self.button_go_login
                ]
            )
        )

        self.page.add(card)
        self.page.update()

    def handle_register(self,e):
        try:
            id_user = int((self.input_id.value or "").strip())
            username = (self.input_username.value or "").strip()
            password = (self.input_password.value or "").strip()

            status = Auth.register(db=self.db,
                                   id=id_user,
                                   username=username,
                                   password=password)
            
            self.text_status.value = status["message"]
            self.text_status.color = "green" if status["success"] else "red"
            self.page.update()
        except ValueError:
            self.text_status.value = "Id solo debe de ser númerico"
            self.page.update()

    def page_login(self):
        self.page.controls.clear()
        
        self.input_username = ft.TextField(
            label="Nombre de usuario",
            hint_text="Ingresa tu nombre de usuario"
        )
        self.input_password = ft.TextField(
            label="Contraseña",
            hint_text="Ingresa tu contraseña",
            password=True,
            can_reveal_password=True
        )
        
        self.button_login_action = ft.ElevatedButton(
        "Iniciar sesión",
        on_click=self.handle_login
        )
        self.text_status = ft.Text(
        value=""
        )
        self.button_go_register = ft.TextButton(
        "¿Aún no tienes cuenta? Regístrate",
        on_click=lambda _: self.page_register()
        )
        
        card = ft.Container(
            width=400,
            padding=25,
            bgcolor="white",
            border_radius=12,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                controls=[
                    ft.Text("Login", size=22, weight=ft.FontWeight.BOLD),
                    self.input_username,
                    self.input_password,
                    self.button_login_action,
                    self.text_status,
                    ft.Divider(),
                    self.button_go_register
                ]
            )
        )
        self.page.add(card)
        self.page.update()
    
    def handle_login(self, e):
        username = (self.input_username.value or "").strip()
        password = (self.input_password.value or "").strip()

        status = Auth.login(db=self.db,
                            username=username,
                            password=password)
        
        if status ["success"]:
            self.loged_user = username
            self.page_main_menu()

        else:
            self.text_status.value = status["message"]
            self.text_status.color = "red"
            self.page.update()


    def page_main_menu(self):
        self.page.controls.clear()
        
        self.page.add(
            ft.Text(f"Bienvenido, {self.loged_user}", 
            size=32,
            weight="bold",
            color="#cc0000"),
            ft.ElevatedButton("Consultar Indicadores", on_click=lambda _: self.page_indicator_menu()),
            ft.ElevatedButton("Historial de consultas", on_click=lambda _: self.page_history_menu()),
            ft.TextButton("Cerrar sesión", on_click=lambda _: self.page_login())
        )
        self.page.update()

    def page_indicator_menu(self):
        self.page.controls.clear()
        self.dropdown_indicator = ft.Dropdown(
            label="Indicador",
            options=[
                ft.dropdown.Option("dolar"),
                ft.dropdown.Option("euro"),
                ft.dropdown.Option("uf"),
                ft.dropdown.Option("utm"),
                ft.dropdown.Option("ipc"),
                ft.dropdown.Option("ivp")
            ]
        )

        self.input_date = ft.TextField(
            label="Fecha (DD-MM-YYYY)",
            hint_text="Ej: 01-01-2025"
        )

        self.text_result = ft.Text(
            value="",
            size=18,
            weight="bold"
            )
        
        btn_consultar = ft.ElevatedButton(
        "Consultar",
        on_click=self.handle_indicator
        )
        
        btn_volver = ft.TextButton(
        "Volver al Menú",
        on_click=lambda _: self.page_main_menu()
        )

        self.page.add(
            ft.Text(
            "Consulta de Indicadores",
            size=24),
            self.dropdown_indicator,
            self.input_date,
            btn_consultar,
            self.text_result,
            btn_volver
        )
        self.page.update()

    def handle_indicator(self, e):
        indicador = self.dropdown_indicator.value
        fecha = (self.input_date.value or "").strip()

        if not indicador:
            self.text_result.value = "Selecciona un indicador"
            self.page.update()
            return

        finance = Finance()
        resultado = finance.get_indicator(indicador, fecha if fecha else None)

        if isinstance(resultado, dict):
            self.text_result.value = resultado["message"]
        else:
            self.text_result.value = f"Valor: ${resultado}"

            self.db.query(
                sql="""INSERT INTO CONSULTAS(username, indicador, fecha_indicador, valor, fecha_consulta, fuente)
                VALUES(:u, :i, :f, :v, CURRENT_TIMESTAMP, :fuente)
                """,
                parameters={
                    "u": self.loged_user,
                    "i": indicador,
                    "f": fecha if fecha else "HOY",
                    "v": resultado,
                    "fuente": "https://mindicador.cl"
                }
            )
        self.page.update()

    def page_history_menu(self):
        self.page.controls.clear()
        
        resultados = self.db.query(
            sql="SELECT indicador, fecha_indicador, valor, fecha_consulta FROM CONSULTAS WHERE username =:u ORDER BY fecha_consulta DESC",
            parameters={"u": self.loged_user}
        )

        lista = ft.ListView(expand=1, spacing=10, padding=20)
        for r in resultados or []:
            lista.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{r[0].upper()} - ${r[2]}"),
                    subtitle=ft.Text(f"Indicador de: {r[1]} | Consultado: {r[3]}")                
                    )
            )

        self.page.add(
            ft.Text("Mi Historial", size=24),
            lista,
            ft.ElevatedButton("Volver", on_click=lambda _: self.page_main_menu())
        )
        self.page.update()

if __name__ == "__main__":
    ft.app(target=App)