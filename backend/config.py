# config.py
import os

# Configuración de JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret-key")

# Configuración de la base de datos
DB_CONFIG = {
    "host": "7kf6x.h.filess.io",
    "port": 3307,
    "user": "dbEcoTourismEsp_masstears",
    "password": "019187989726a2b3a00a371164b41a7818a8fa6d",
    "database": "dbEcoTourismEsp_masstears",
}
