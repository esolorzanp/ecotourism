import mysql.connector
import bcrypt
from db import get_db_connection

# Datos del usuario administrador
nombre_admin = "Administrador"
correo_admin = "admin@dominio.com"
clave_admin = "1234"
perfil_admin = "Administrador"

def crear_usuario_admin():
    # Conexión a la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Obtener el ID del perfil "administrador"
        cursor.execute("SELECT id FROM perfiles WHERE descripcion = %s", (perfil_admin,))
        perfil_id = cursor.fetchone()

        if perfil_id is None:
            print("Error: El perfil 'administrador' no existe en la tabla perfil.")
            return

        perfil_id = perfil_id[0]

        # Encriptar la clave
        clave_encriptada = bcrypt.hashpw(clave_admin.encode('utf-8'), bcrypt.gensalt())

        # Insertar el usuario administrador en la tabla usuario
        query = """
        INSERT INTO usuarios (nombre, correo, clave, id_perfil)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (nombre_admin, correo_admin, clave_encriptada, perfil_id))
        conn.commit()

        print("Usuario administrador creado con éxito.")

    except mysql.connector.Error as err:
        print("Error al crear el usuario:", err)

    finally:
        cursor.close()
        conn.close()

# Ejecutar la función para crear el usuario administrador
crear_usuario_admin()
