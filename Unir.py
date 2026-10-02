import os
import re
import flet as ft
from pathlib import Path
import re
import glob
import os



carpeta = r"C:\Users\villafra\Mars Inc\Planning South LATAM - Documentos\Recetas\X SKU"
salida = r"C:\Users\villafra\Documents\Visual Studio\recetas_unificadas.txt"

# Abrimos en modo escritura para poner la cabecera
with open(salida, "w", encoding="utf-8", newline="\n") as out:
    out.write("Fecha\tMaterial\tDenominacion\tAlternativa\tNivel\tPos\tObj\tTexto\tCantidad\tUM\tCaP\n")

# Ahora recorremos y vamos agregando los datos de cada archivo
for archivo in glob.glob(os.path.join(carpeta, "*.txt")):
    with open(archivo, "r", encoding="cp1252") as f:
        lineas = f.readlines()

    fecha = material = denominacion = None
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
            # Extraer Alternativa
            elif linea.strip().startswith("Centr/Util./Alt:"):
            # tomar lo que viene después de los ":" y separar por "/"
                partes_alt = linea.strip().split(":")[-1].strip().split("/")
                alternativa = partes_alt[-1].strip()  # toma el último elemento
            # Inicio tabla
            if linea.strip().startswith("Nivel"):
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

