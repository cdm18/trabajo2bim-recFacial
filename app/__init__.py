from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
    
    # Registrar Blueprints (Rutas/Controladores)
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    return app
