# sitios/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db_connection

sitios_bp = Blueprint("sitios", __name__)

# Listar sitios
@sitios_bp.route("/sitios", methods=["GET"])
@jwt_required()
def listar_sitios():
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]   #El listar sitios funciona para los tres roles, REVISAR

    if perfil_id != 2 and perfil_id != 3:  # Solo empleado (2) y supervisor (3) pueden listar sitios 
        return jsonify({"msg": "No tiene permisos para listar sitios"}), 403
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        sql = """
        SELECT id, descripcion, detalle FROM sitios
        """
        cursor.execute(sql)
        sitios = cursor.fetchall()
        return jsonify(sitios), 201
    finally:
        cursor.close()
        conn.close()

# Obtener un sitio por ID
@sitios_bp.route("/sitios/<int:id>", methods=["GET"])
@jwt_required()
def obtener_sitio(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]

    if perfil_id  != 2:  # Solo empleado (2) pueden obtener sitio por id
        return jsonify({"msg": "No tiene permisos para obtner sitios"}), 403
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        sql = """
        SELECT id, descripcion, detalle FROM sitios WHERE id = %s
        """
        cursor.execute(sql, (id,))
        sitio = cursor.fetchone()
        if sitio:
            return jsonify(sitio), 201
        return jsonify({"message": "Sitio no encontrado"}), 404
    finally:
        cursor.close()
        conn.close()

# Agregar un sitio
@sitios_bp.route("/sitios", methods=["POST"])
@jwt_required()
def crear_sitio():
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]

    if perfil_id != 2:  # Solo el empleado (2) puede agregar sitios
        return jsonify({"msg": "No tiene permisos para agregar sitios"}), 403

    data = request.get_json()
    descripcion = data.get("descripcion")
    detalle = data.get("detalle")

    if not descripcion or not detalle:
        return jsonify({"msg": "Descripción y detalle son requeridos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql = """
        INSERT INTO sitios (descripcion, detalle) 
        VALUES (%s, %s)
        """
        cursor.execute(sql, (descripcion, detalle))
        conn.commit()
        return jsonify({"message": "Sitio creado exitosamente"}), 201
    finally:
        cursor.close()
        conn.close()


# Modificar un sitio
@sitios_bp.route("/sitios/<int:id>", methods=["PUT"])
@jwt_required()
def modificar_sitio(id):
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]

    if perfil_id != 2:  # Solo el empleado (2) puede modificar sitios
        return jsonify({"msg": "No tiene permisos para modificar sitios"}), 403

    data = request.get_json()
    descripcion = data.get("descripcion")
    detalle = data.get("detalle")

    if not descripcion or not detalle:
        return jsonify({"msg": "Descripción y detalle son requeridos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql = """
        UPDATE sitios
        SET descripcion = %s, detalle = %s
        WHERE id = %s
        """
        cursor.execute(sql, (descripcion, detalle, id))
        conn.commit()
        return jsonify({"message": "Sitio modificado exitosamente"}), 201
    finally:
        cursor.close()
        conn.close()


# Eliminar un sitio
@sitios_bp.route("/sitios/<int:id>", methods=["DELETE"])
@jwt_required()
def eliminar_sitio(id):
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]

    if perfil_id != 2:  # Solo el empleado (2) puede eliminar sitios
        return jsonify({"msg": "No tiene permisos para eliminar sitios"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql = """
        DELETE FROM sitios WHERE id = %s
        """
        cursor.execute(sql, (id,))
        conn.commit()
        return jsonify({"message": "Sitio eliminado exitosamente"}), 201
    finally:
        cursor.close()
        conn.close()