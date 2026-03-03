# DB

Para desplegar localmente, sólo hay que hacer lo siguente

## Requisitos

Asegúrate de tener instalado lo siguiente:

- [Python 3.6 o superior](https://www.python.org/downloads/)
- `pip` (gestor de paquetes de Python)
- `git`

---

## Crear un Entorno Virtual

Sigue estos pasos para crear un entorno virtual:

1. **Abre una terminal.**

2. **Navega al directorio de tu proyecto:**

   ```bash
   cd $HOME
   git clone https://Road2asir/DB ./app_ud5
   cd ./app_ud5
   python -m venv venv
   source venv/bin/activate
   pip install -U pip setuptools wheel
   pip install Flask
   export FLASK_APP=app_ud5.py
   export FLASK_DEBUG=true
   flask run
   ```

   ## La app deberia estar desplegada en http://127.0.0.1:5000
