@echo off
rem Regenera el borrador (publica los articulos del blog cuya fecha ya llego) y lo abre en
rem http://127.0.0.1:8790/oficinas/costa-rica/
cd /d "%~dp0"
uv run --python 3.12 python generar.py
cd /d "%~dp0sitio"
start "" http://127.0.0.1:8790/oficinas/costa-rica/
uv run --python 3.12 python -m http.server 8790 --bind 127.0.0.1
