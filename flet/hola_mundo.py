import flet as ft 

class App:
    def __init__(self, page: ft.Page):
        self.page = page 
        self.page.title = "Hola mundo"
        # Siempre como ultima linea de __init
        self.build()
    # Metodo principal para agregar elementos
    # En mi pagina/aplicacion
    def build(self):
        self.page.add(
            ft.Text(value="Hola mundo")
        )
# Inicializamos la App
if __name__ == "__main__":
    ft.app(target=App)
