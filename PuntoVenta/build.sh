#!/bin/bash

set -o errexit
# Instalar dependencias
pip install -r requirements.txt

poetry install

# Ejecutar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput
