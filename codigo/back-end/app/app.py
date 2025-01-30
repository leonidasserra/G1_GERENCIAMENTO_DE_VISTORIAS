from flask import Flask
from dotenv import load_dotenv
import os
from flask_swagger_ui import get_swaggerui_blueprint
from extensions import mail
from database import db, init_db


# Carregar variáveis de ambiente
load_dotenv()

def create_app():
    # Inicializar o Flask
    app = Flask(__name__)

    # Configuração do banco de dados
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(basedir, 'prototipo1.db')}"  # Padrão para desenvolvimento
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuração do Flask-Mail
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1']
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    # Inicializar extensões
    mail.init_app(app)
    init_db(app)

    # Registrar Blueprints
    from routes.funcionario_routes import funcionario_bp
    from routes.imobiliaria_routes import imobiliaria_bp
    from routes.vistoriador_routes import vistoriador_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.auth_routes import auth_bp

    app.register_blueprint(funcionario_bp)
    app.register_blueprint(imobiliaria_bp)
    app.register_blueprint(vistoriador_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)

    # Configuração do Swagger
    SWAGGER_URL = '/docs'
    API_URL = '/static/swagger.json'
    swagger_bp = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
