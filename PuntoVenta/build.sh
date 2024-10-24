#!/bin/bash

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput
