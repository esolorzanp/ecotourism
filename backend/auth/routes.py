# auth/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
from db import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    correo = data.get('correo')
    clave = data.get('clave')

    conn = get_db_connection()
    cursor = conn.cursor()

    print(correo)
    print(clave)

    try:
        cursor.execute("SELECT id, clave, id_perfil FROM usuarios WHERE correo = %s", (correo,))
        user = cursor.fetchone()
        
        print(user)

        if user and bcrypt.checkpw(clave.encode('utf-8'), user[1].encode('utf-8')):
            access_token = create_access_token(identity={'id': user[0], 'perfil_id': user[2]})
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"msg": "Credenciales inválidas"}), 401
    finally:
        cursor.close()
        conn.close()