# usuarios/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import bcrypt
from db import get_db_connection

usuarios_bp = Blueprint("usuarios", __name__)


# Listar usuarios
@usuarios_bp.route("/usuarios", methods=["GET"])
@jwt_required()
def listar_usuarios():
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]

    if perfil_id != 1:  # Solo Administrador (3) puede crear usuarios
        return jsonify({"msg": "No tiene permisos para crear usuarios"}), 403

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        sql = """
        SELECT u.id, u.nombre, u.correo, p.descripcion AS perfil FROM usuarios u 
        INNER JOIN perfiles p ON p.id = u.id_perfil
        """
        cursor.execute(sql)
        usuarios = cursor.fetchall()
        return jsonify(usuarios), 201
    finally:
        cursor.close()
        conn.close()


# Obtener un usuario
@usuarios_bp.route("/usuarios/<int:id>", methods=["GET"])
@jwt_required()
def obtener_usuarios(id):
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]

    if perfil_id != 1:  # Solo Administrador (3) puede crear usuarios
        return jsonify({"msg": "No tiene permisos para crear usuarios"}), 403

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        sql = """
        SELECT u.id, u.nombre, u.correo, p.descripcion FROM usuarios u 
        INNER JOIN perfiles p ON p.id = u.id_perfil WHERE u.id = %s
        """
        cursor.execute(sql, (id,))
        usuarios = cursor.fetchall()
        if usuarios:
            return jsonify(usuarios), 201
        return jsonify({"message": "No se encontró el usuario"}), 201
    finally:
        cursor.close()
        conn.close()


# Agregar un usuario
@usuarios_bp.route("/usuarios", methods=["POST"])
@jwt_required()
def crear_usuarios():
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]

    if perfil_id != 1:  # Solo Administrador (3) puede crear usuarios
        return jsonify({"msg": "No tiene permisos para crear usuarios"}), 403

    data = request.get_json()
    correo = data.get("correo")
    clave = data.get("clave")
    nombre = data.get("nombre")
    id_perfil = int(data.get("perfil"))

    clave_encriptada = bcrypt.hashpw(clave.encode("utf-8"), bcrypt.gensalt())

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql = """
        INSERT INTO USUARIOS (nombre, correo, clave, id_perfil) VALUES (%s,%s,%s,%s)
        """
        cursor.execute(sql, (nombre, correo, clave_encriptada, id_perfil))
        conn.commit()
        return jsonify({"message": "Usuario creado exitosamente"}), 201
    finally:
        cursor.close()
        conn.close()


# Modificar un usuario
@usuarios_bp.route("/usuarios/<int:id>", methods=["PUT"])
@jwt_required()
def modificar_usuarios(id):
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]

    if perfil_id != 1:  # Solo Administrador (3) puede crear usuarios
        return jsonify({"msg": "No tiene permisos para crear usuarios"}), 403

    data = request.get_json()
    correo = data.get("correo")
    nombre = data.get("nombre")
    id_perfil = int(data.get("perfil"))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql = """
        UPDATE USUARIOS SET nombre = %s, correo = %s, id_perfil = %s WHERE id = %s
        """
        cursor.execute(sql, (nombre, correo, id_perfil, id))
        conn.commit()
        return jsonify({"message": "Usuario modificado exitosamente"}), 201
    finally:
        cursor.close()
        conn.close()


# Eliminar un usuario
@usuarios_bp.route("/usuarios/<int:id>", methods=["DELETE"])
@jwt_required()
def eliminar_usuarios(id):
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]

    if perfil_id != 1:  # Solo Administrador (3) puede crear usuarios
        return jsonify({"msg": "No tiene permisos para crear usuarios"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql = """
        DELETE FROM USUARIOS WHERE id = %s
        """
        cursor.execute(sql, (id,))
        conn.commit()
        return jsonify({"message": "Usuario eliminado exitosamente"}), 201
    finally:
        cursor.close()
        conn.close()
