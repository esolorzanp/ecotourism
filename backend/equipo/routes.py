# equipo/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db_connection

equipo_bp = Blueprint("equipo", __name__)

# Listar miembros del equipo
@equipo_bp.route("/equipo", methods=["GET"])
@jwt_required()
def listar_equipo():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"] # mismo error lo pueden listar los 3 roles REVISAR

    if perfil_id != 2 & perfil_id != 3:  # Solo empleado (2) y supervisor (3) pueden listar el equipo
        return jsonify({"msg": "No tiene permisos para listar equipo"}), 403
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        sql = """
        SELECT id, nombre, cargo, edad, genero, hobbies, conocimientos FROM equipo
        """
        cursor.execute(sql)
        equipo = cursor.fetchall()
        return jsonify(equipo), 200
    finally:
        cursor.close()
        conn.close()

# Obtener un miembro del equipo por ID
@equipo_bp.route("/equipo/<int:id>", methods=["GET"])
@jwt_required()
def obtener_miembro_equipo(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]

    if perfil_id  != 2:  # Solo empleado (2) puede obtener al miembro del equipo por id
        return jsonify({"msg": "No tiene permisos para obtner equipo"}), 403
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        sql = """
        SELECT id, nombre, cargo, edad, genero, hobbies, conocimientos FROM equipo WHERE id = %s
        """
        cursor.execute(sql, (id,))
        miembro = cursor.fetchall()
        if miembro:
            return jsonify(miembro), 200
        return jsonify({"message": "Miembro del equipo no encontrado"}), 404
    finally:
        cursor.close()
        conn.close()

# Agregar un miembro al equipo
@equipo_bp.route("/equipo", methods=["POST"])
@jwt_required()
def crear_miembro_equipo():
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]

    if perfil_id != 2:  # Solo el empleado (2) puede agregar miembros al equipo
        return jsonify({"msg": "No tiene permisos para agregar miembros al equipo"}), 403

    data = request.get_json()
    nombre = data.get("nombre")
    cargo = data.get("cargo")
    edad = data.get("edad")
    genero = data.get("genero")
    hobbies = data.get("hobbies")
    conocimientos = data.get("conocimientos")

    if not all([nombre, cargo, edad, genero, hobbies]):
        return jsonify({"msg": "Todos los campos (excepto conocimientos) son requeridos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql = """
        INSERT INTO equipo (nombre, cargo, edad, genero, hobbies, conocimientos) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre, cargo, edad, genero, hobbies, conocimientos))
        conn.commit()
        return jsonify({"message": "Miembro del equipo creado exitosamente"}), 201
    finally:
        cursor.close()
        conn.close()

# Modificar un miembro del equipo
@equipo_bp.route("/equipo/<int:id>", methods=["PUT"])
@jwt_required()
def modificar_miembro_equipo(id):
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]

    if perfil_id != 2:  # Solo el empleado (2) puede modificar miembros del equipo
        return jsonify({"msg": "No tiene permisos para modificar miembros del equipo"}), 403

    data = request.get_json()
    nombre = data.get("nombre")
    cargo = data.get("cargo")
    edad = data.get("edad")
    genero = data.get("genero")
    hobbies = data.get("hobbies")
    conocimientos = data.get("conocimientos")

    if not all([nombre, cargo, edad, genero, hobbies]):
        return jsonify({"msg": "Todos los campos (excepto conocimientos) son requeridos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql = """
        UPDATE equipo
        SET nombre = %s, cargo = %s, edad = %s, genero = %s, hobbies = %s, conocimientos = %s
        WHERE id = %s
        """
        cursor.execute(sql, (nombre, cargo, edad, genero, hobbies, conocimientos, id))
        conn.commit()
        return jsonify({"message": "Miembro del equipo modificado exitosamente"}), 200
    finally:
        cursor.close()
        conn.close()


# Eliminar un miembro del equipo
@equipo_bp.route("/equipo/<int:id>", methods=["DELETE"])
@jwt_required()
def eliminar_miembro_equipo(id):
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]

    if perfil_id != 2:  # Solo el empleado (2) puede eliminar miembros del equipo
        return jsonify({"msg": "No tiene permisos para eliminar miembros del equipo"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql = """
        DELETE FROM equipo WHERE id = %s
        """
        cursor.execute(sql, (id,))
        conn.commit()
        return jsonify({"message": "Miembro del equipo eliminado exitosamente"}), 200
    finally:
        cursor.close()
        conn.close()
