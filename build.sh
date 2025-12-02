#!/usr/bin/env bash
set -o errexit

echo "=== Configurando entorno Python ==="
python --version
pip --version

echo "=== Instalando dependencias ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Aplicando migraciones ==="
python manage.py migrate --noinput

echo "=== Colectando archivos estáticos ==="
python manage.py collectstatic --noinput

echo "=== ¡Build completado! ==="