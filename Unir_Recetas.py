# Unir_Recetas.py
import os
import re
import glob

def unir_recetas(input_dir: str, output_dir: str, archive_type: str):
    # Nombre fijo de salida
    output_filename = f"Recetas Unificadas ({archive_type}).txt"
    salida = os.path.join(output_dir, output_filename)
    numero = 0
    # Abrimos en modo escritura para poner la cabecera
    with open(salida, "w", encoding="utf-8", newline="\n") as out:
        out.write("Fecha\tMaterial\tDenominacion\tAlternativa\tNivel\tPos\tObj\tTexto\tCantidad\tUM\tCaP\n")

    # Recorremos y agregamos datos de cada archivo
    for archivo in glob.glob(os.path.join(input_dir, "*.txt")):
        with open(archivo, "r", encoding="cp1252") as f:
            lineas = f.readlines()

        fecha = material = denominacion = alternativa = None
        in_tabla = False

        with open(salida, "a", encoding="utf-8", newline="\n") as out:  # append
            for linea in lineas:
                # Fecha
                if re.match(r"^\d{2}\.\d{2}\.\d{2}", linea.strip()):
                    fecha = linea.strip().split()[0]
                # Material
                elif linea.strip().startswith("Material"):
                    material = linea.strip().split()[-1]
                # Denominación
                elif linea.strip().startswith("Denominación"):
                    denominacion = " ".join(linea.strip().split()[1:])
                # Alternativa
                elif linea.strip().startswith("Centr/Util./Alt:"):
                    partes_alt = linea.strip().split(":")[-1].strip().split("/")
                    alternativa = partes_alt[-1].strip() if partes_alt else ""

                # Inicio tabla
                if linea.strip().startswith("Nivel") or linea.strip().startswith("Nv."):
                    in_tabla = True
                    continue

                # Filas de tabla
                if in_tabla and linea.strip():
                    partes = re.split(r"\s{2,}|\t+", linea.strip())

                    if len(partes) >= 7:
                        nivel = re.sub(r"\.+", "", partes[0])
                        pos, obj = partes[1:3]
                        texto = partes[3]
                        cantidad = partes[4]
                        um = partes[5]
                        cap = partes[6] if len(partes) > 6 else ""
                        out.write(f"{fecha}\t{material}\t{denominacion}\t{alternativa}\t{nivel}\t{pos}\t{obj}\t{texto}\t{cantidad}\t{um}\t{cap}\n")

