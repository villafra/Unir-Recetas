# Usuarios.py
import json
import flet as ft
import MensajesPopUp as pop
from Unir_Recetas import unir_recetas

CONFIG_FILE = "config.json"


def folder_picker_view(page: ft.Page, user: str, config: dict) -> ft.View:

    view = ft.View(route="/main", controls=[])

    page.title = "Unir archivos"

    # FilePickers (se conservan exactamente igual)
    folder_picker_in = ft.FilePicker()
    folder_picker_out = ft.FilePicker()

    input_text = ft.TextField(
        label="Ingrese carpeta de Recetas",
        read_only=True,
        expand=True,
        value=config["usuarios"][user].get("input_dir", ""),
        text_size=12,
        height=30,  # 🟢 Tu alto de 30 conservado
    )

    output_text = ft.TextField(
        label="Indique la carpeta de destino",
        read_only=True,
        expand=True,
        value=config["usuarios"][user].get("output_dir", ""),
        text_size=12,
        height=30,  # 🟢 Tu alto de 30 conservado
    )

    # 🟢 NUEVO: Selector de tipo de receta centrado
    tipo_receta_selector = ft.RadioGroup(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,  # Centra horizontalmente
            spacing=30,
            controls=[
                ft.Radio(value="SKU", label="SKU"),
                ft.Radio(value="Halb", label="Halb"),
            ],
        ),
        value="SKU",  # SKU seleccionado por defecto
    )

    async def pick_input(e):

        folder = await folder_picker_in.get_directory_path()

        if folder:
            input_text.value = folder

            config["usuarios"][user]["input_dir"] = folder

            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4, ensure_ascii=False)

            page.update()

    async def pick_output(e):

        folder = await folder_picker_out.get_directory_path()

        if folder:
            output_text.value = folder

            config["usuarios"][user]["output_dir"] = folder

            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4, ensure_ascii=False)

            page.update()

    # Botones tal y como los tenías
    btn_input = ft.Button("Elegir carpeta de Recetas", on_click=pick_input)

    btn_output = ft.Button("Elegir carpeta de Destino", on_click=pick_output)

    def ejecutar_unir(e):

        in_dir = input_text.value.strip()
        out_dir = output_text.value.strip()
        tipo_receta = tipo_receta_selector.value  # 🟢 Obtener SKU o Halb

        if not in_dir or not out_dir:

            pop.mostrar_mensaje(page, "Debe elegir ambas carpetas", True)

            return

        try:
            # 🟢 Pasamos la selección del tipo a tu función unificadora
            unir_recetas(in_dir, out_dir, tipo_receta)

            nombre_final = f"Recetas Unificadas ({tipo_receta}).txt"
            pop.mostrar_mensaje(
                page, f"Archivos unidos correctamente en:\n{out_dir}\\{nombre_final}"
            )

        except Exception as ex:

            pop.mostrar_mensaje(page, f"Error: {ex}", True)

            print(ex)

    unir_button = ft.FilledButton(content="Unir archivos", on_click=ejecutar_unir)

    # 🟢 Tu estructura original intacta con la nueva sección agregada abajo
    view.controls.append(
        ft.Container(
            content=ft.Column(
                [
                    input_text,
                    btn_input,
                    output_text,
                    btn_output,
                    ft.Container(height=10),  # Separador pequeño estético
                    tipo_receta_selector,  # 🟢 Selector agregado justo antes del botón final
                    ft.Container(height=10),
                    unir_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
                expand=True,
            ),
            alignment=ft.Alignment.CENTER,
            expand=True,
        )
    )

    return view
