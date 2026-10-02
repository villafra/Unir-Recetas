import flet as ft
import json
import os
from screeninfo import get_monitors
from Unir_Recetas import unir_recetas
import ssl

CONFIG_FILE = "config.json"

try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

# Funciones para manejar JSON
def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"usuarios": {}}
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    if "usuarios" not in cfg:
        cfg["usuarios"] = {}
    return cfg

def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)

# Pantalla de login / gestión de usuarios
def login_screen(page: ft.Page, config):
    # Función ingresar (navega a nueva página con funcionalidad de prueba.py)
    async def ingresar_usuario(e):
        if user_combo.value:
            import Usuarios
            view = Usuarios.folder_picker_view(page, user_combo.value, config)
            page.views.append(view)
            await page.push_route(view.route)
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Debe seleccionar un usuario"))
            page.snack_bar.open = True
            page.update()

    def crear(e):
        new_user = new_user_field.value.strip()
        if not new_user:
            mostrar_mensaje("Debe ingresar un nombre de usuario", error=True)
            return
        if new_user in config["usuarios"]:
            mostrar_mensaje(f"El usuario '{new_user}' ya existe", error=True)
            return
        # Guardamos en JSON con input_dir y output_dir vacíos
        config["usuarios"][new_user] = {"input_dir": "", "output_dir": ""}
        save_config(config)
        # Actualizamos el combo box
        user_combo.options.append(ft.dropdown.Option(new_user))
        user_combo.value = new_user
        page.update()
        mostrar_mensaje(f"Usuario '{new_user}' creado exitosamente")
        # Hide the input fields
        new_user_field.visible = False
        btn_crear_confirm.visible = False
        btn_cancel.visible = False
        new_user_field.value = ""
        btn_crear.visible = True
        page.update()

    def cerrar(e=None):
        new_user_field.visible = False
        btn_crear_confirm.visible = False
        btn_cancel.visible = False
        new_user_field.value = ""
        btn_crear.visible = True
        page.update()

    # Función crear usuario
    def crear_usuario(e):
        new_user_field.visible = True
        btn_crear_confirm.visible = True
        btn_cancel.visible = True
        btn_crear.visible = False
        page.update()

    user_combo = ft.Dropdown(
        label="Seleccionar usuario existente",
        width=200,
        options=[ft.dropdown.Option(u) for u in config["usuarios"].keys()]
    )

    btn_ingresar = ft.Button("Ingresar")
    btn_crear = ft.Button("Crear usuario")

    new_user_field = ft.TextField(label="Ingrese nombre del nuevo usuario", visible=False, on_submit=crear)
    btn_crear_confirm = ft.Button("Crear", visible=False)
    btn_cancel = ft.Button("Cancelar", visible=False)

    btn_ingresar.on_click = ingresar_usuario
    btn_crear.on_click = crear_usuario
    btn_crear_confirm.on_click = crear
    btn_cancel.on_click = cerrar
    page.update()

    page.add(
        ft.Column(
            [
                ft.Text("Gestión de Usuarios", size=20, weight="bold"),
                user_combo,
                ft.Row([btn_ingresar, btn_crear], alignment="center", spacing=10),
                new_user_field,
                ft.Row([btn_crear_confirm, btn_cancel], alignment="center", spacing=10)
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=15,
            expand=True
        )
    )
    page.update()

    def mostrar_mensaje(texto, error=False):
            message_box = ft.AlertDialog(
                title=ft.Text("Error") if error else ft.Text("Información"),
                content=ft.Text(texto),
                
                actions_alignment=ft.MainAxisAlignment.END,
                )
            page.show_dialog(message_box)

# App principal
def main(page: ft.Page):
    page.title = "Gestión de Usuarios"
    page.window.maximized = False
    page.window.width = 600
    page.window.height = 400
    page.window_min_width = 400
    page.window_min_height = 300
    page.window_max_width = 800
    page.window_max_height = 600
    monitor = get_monitors()[0]
    screen_w, screen_h = monitor.width, monitor.height
    page.window.left = (screen_w - page.width) // 2 
    page.window.top = (screen_h - page.height) // 2
    page.window_resizable = False
    page.update()

    config = load_config()
    login_screen(page, config)

    

ft.run(main)

