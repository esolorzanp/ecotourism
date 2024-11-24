from config import JWT_SECRET_KEY
from auth.routes import auth_bp
from usuarios.routes import usuarios_bp
from comentarios.routes import comentarios_bp
from sitios.routes import sitios_bp
from equipo.routes import equipo_bp
from preguntasfrecuentes.routes import preguntas_bp


# Inicialización de la aplicación Flask
app = Flask(__name__)
CORS(app)
# Registro de Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(comentarios_bp)
app.register_blueprint(sitios_bp)
app.register_blueprint(equipo_bp)
app.register_blueprint(preguntas_bp)

if __name__ == "__main__":
    app.run(debug=True)
    