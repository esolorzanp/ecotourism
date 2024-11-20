# config.py
import os

# Configuración de JWT
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secret-key')

# Configuración de la base de datos
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "dbEcoTourismEsp"
}