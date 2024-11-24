# comentarios/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import bcrypt
from db import get_db_connection

comentarios_bp = Blueprint("comentarios", __name__)

# Listar comentarios
@comentarios_bp.route("/comentarios", methods=["GET"])
@jwt_required()
def listar_comentarios():
    identity = get_jwt_identity()
    perfil_id = identity["perfil_id"]

    if perfil_id != 2 | perfil_id !=3:  # Solo Supervisor (3) y empleado (2) pueden listar comentarios
        return jsonify({"msg": "No tiene permisos para listar comentarios"}), 403

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        sql = """
        SELECT * FROM comentarios
        """
        cursor.execute(sql)
        comentarios = cursor.fetchall()
        return jsonify(comentarios), 201
    finally:
        cursor.close()
        conn.close()


# Agregar un comentario
@comentarios_bp.route("/comentarios", methods=["POST"])

def crear_comentarios():

    data = request.get_json()
    nombres = data.get("nombres")
    ocupacion = data.get("ocupacion")
    ciudadOrigen = data.get("ciudadOrigen")
    comentario = data.get("comentario")
    calificacion = data.get("calificacion")
    fecha = data.get("fecha")
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        sql = """
        INSERT INTO COMENTARIOS (nombres, ocupacion, ciudadOrigen, comentario, calificacion, fecha) VALUES (%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(sql, (nombres, ocupacion, ciudadOrigen, comentario, calificacion, fecha))
        conn.commit()
        return jsonify({"message": "Comentario creado exitosamente"}), 201
    finally:
        cursor.close()
        conn.close()
        