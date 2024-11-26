# preguntasfrecuentes/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db_connection

preguntas_bp = Blueprint("preguntasfrecuentes", __name__)

# Listar preguntas frecuentes
@preguntas_bp.route("/preguntasfrecuentes", methods=["GET"])
@jwt_required()
def listar_preguntas():
    print('Entra al backend')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"] # 

    if perfil_id != 2 and perfil_id != 3:  # Solo empleado (2) y supervisor (3) pueden listar preguntas frecuentes
        return jsonify({"msg": "No tiene permisos para listar preguntas frecuentes"}), 403
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        sql = """
        SELECT id, pregunta, respuesta, orden FROM preguntasfrecuentes ORDER BY orden
        """
        cursor.execute(sql)
        preguntas = cursor.fetchall()
        return jsonify(preguntas), 201
    finally:
        cursor.close()
        conn.close()

# Obtener una pregunta frecuente por ID
@preguntas_bp.route("/preguntasfrecuentes/<int:id>", methods=["GET"])
@jwt_required()
def obtener_pregunta(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]

    if perfil_id  != 2:  # Solo empleado (2) puede obtener las preguntas frecuentes por id
        return jsonify({"msg": "No tiene permisos para obtner preguntas frecuentes"}), 403
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        sql = """
        SELECT id, pregunta, respuesta, orden FROM preguntasfrecuentes WHERE id = %s
        """
        cursor.execute(sql, (id,))
        pregunta = cursor.fetchone()
        if pregunta:
            return jsonify(pregunta), 201
        return jsonify({"message": "Pregunta no encontrada"}), 404
    finally:
        cursor.close()
        conn.close()

 # Agregar una pregunta frecuente

# Adicionar una pregunta frecuente
@preguntas_bp.route("/preguntasfrecuentes", methods=["POST"])
@jwt_required()
def crear_pregunta():
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]

    if perfil_id != 2:   # Solo el empleado (2) puede agregar preguntas freceuntes
        return jsonify({"msg": "No tiene permisos para agregar preguntas frecuentes"}), 403

    data = request.get_json()
    pregunta = data.get("pregunta")
    respuesta = data.get("respuesta")
    orden = data.get("orden")

    if not all([pregunta, respuesta, orden]):
        return jsonify({"msg": "Todos los campos son requeridos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql = """
        INSERT INTO preguntasfrecuentes (pregunta, respuesta, orden) 
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (pregunta, respuesta, orden))
        conn.commit()
        return jsonify({"message": "Pregunta creada exitosamente"}), 201
    finally:
        cursor.close()
        conn.close()

# Modificar una pregunta frecuente
@preguntas_bp.route("/preguntasfrecuentes/<int:id>", methods=["PUT"])
@jwt_required()
def modificar_pregunta(id):
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]

    if perfil_id != 2:  # Solo el empleado (2) puede modificar preguntas
        return jsonify({"msg": "No tiene permisos para modificar preguntas frecuentes"}), 403

    data = request.get_json()
    pregunta = data.get("pregunta")
    respuesta = data.get("respuesta")
    orden = data.get("orden")

    if not all([pregunta, respuesta, orden]):
        return jsonify({"msg": "Todos los campos son requeridos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql = """
        UPDATE preguntasfrecuentes
        SET pregunta = %s, respuesta = %s, orden = %s
        WHERE id = %s
        """
        cursor.execute(sql, (pregunta, respuesta, orden, id))
        conn.commit()
        return jsonify({"message": "Pregunta modificada exitosamente"}), 201
    finally:
        cursor.close()
        conn.close()

        # Eliminar una pregunta frecuente

# Eliminar una pregunta frecuente
@preguntas_bp.route("/preguntasfrecuentes/<int:id>", methods=["DELETE"])
@jwt_required()
def eliminar_pregunta(id):
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]

    if perfil_id != 2:  # Solo el empleado (2) puede eliminar preguntas
        return jsonify({"msg": "No tiene permisos para eliminar preguntas frecuentes"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql = """
        DELETE FROM preguntasfrecuentes WHERE id = %s
        """
        cursor.execute(sql, (id,))
        conn.commit()
        return jsonify({"message": "Pregunta eliminada exitosamente"}), 201
    finally:
        cursor.close()
        conn.close()





