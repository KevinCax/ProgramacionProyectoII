from django.db import models
import re

def validar_dpi(dpi):
    
    try:
        dpi = str(dpi).strip()
        if not dpi:
            return False

        # Expresion regular para validar si aplica el patrón
        dpi_reg_exp = re.compile('^[0-9]{4}\s?[0-9]{5}\s?[0-9]{4}$')
        if not dpi_reg_exp.match(dpi):
            return False

        # Eliminar espacios
        dpi = dpi.replace(' ', '')

        # Extraer partes del DPI
        departamento = int(dpi[10])
        municipio = int(dpi[11:13])
        numero = str(dpi[0:8])
        verificador = int(dpi[8:9])

        municipios_por_depto = [
            17, # 01 - Guatemala tiene: 17 municipios.
            8,  # 02 - El Progreso tiene: 8 municipios.
            16, # 03 - Sacatepéquez tiene: 16 municipios.
            16, # 04 - Chimaltenango tiene: 16 municipios.
            13, # 05 - Escuintla tiene: 13 municipios.
            14, # 06 - Santa Rosa tiene: 14 municipios.
            19, # 07 - Sololá tiene: 19 # municipios.
            8,  # 08 - Totonicapán tiene: 8 municipios.
            24, # 09 - Quetzaltenango tiene: 24 municipios.
            21, # 10 - Suchitepéquez tiene: 21 municipios.
            9,  # 11 - Retalhuleu tiene: 9 municipios.
            30, # 12 - San Marcos tiene: 30 municipios.
            32, # 13 - Huehuetenango tiene: 32 municipios.
            21, # 14 - Quiché tiene: 21 municipios.
            8,  # 15 - Baja Verapaz tiene: 8 municipios.
            17, # 16 - Alta Verapaz tiene: 17 municipios.
            14, # 17 - Petén tiene: 14 municipios.
            5,  # 18 - Izabal tiene: 5 municipios.
            11, # 19 - Zacapa tiene: 11 municipios.
            11, # 20 - Chiquimula tiene: 11 municipios.
            7,  # 21 - Jalapa tiene: 7 municipios.
            17, # 22 - Jutiapa tiene: 17 municipios.
        ]

        if departamento == 0 or municipio == 0:
            return False
        if departamento > len(municipios_por_depto):
            return False
        if municipio > municipios_por_depto[departamento - 1]:
            return False

        total = 0
        numero = [int(x) for x in str(numero)]

        for i in range(len(numero)):
            total += numero[i] * (i + 2)

        modulo = total % 11

        return modulo == verificador

    except (ValueError, IndexError) as e:
        print(f"Error en la validación del DPI: {e}")  
        return False
    

def generar_usuario(nombre):
    from .models import Usuario
    if not nombre:
        return None

    usuario_generado = nombre.lower().replace(" ", "_") 
    while Usuario.objects.filter(usuario=usuario_generado).exists():
        usuario_generado += "_1" 
    return usuario_generado
