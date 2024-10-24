# Copia y pega el siguiente contenido en un archivo llamado install-poetry.py
import sys
import subprocess

if __name__ == "__main__":
    url = "https://install.python-poetry.org"
    subprocess.check_call([sys.executable, "-m", "pip", "install", "poetry", "--upgrade"])
