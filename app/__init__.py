from flask import Flask

# Inicializar la aplicación Flask
def create_app():
    app = Flask(__name__)
    
    # Registrar las rutas desde routes.py
    from app.routes import app as routes_blueprint
    app.register_blueprint(routes_blueprint)
    
    return app
 
