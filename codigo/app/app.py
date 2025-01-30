from flask import Flask
from flask_session import Session
from dotenv import load_dotenv
import os
from flask import Flask, redirect, url_for, session, request
from extensions import mail
from database import db, init_db
from routes.views_routes import views_bp
from routes.auth_routes import auth_bp
from routes.funcionario_routes import funcionario_bp
from routes.imobiliaria_routes import imobiliaria_bp
from routes.vistoriador_routes import vistoriador_bp
from routes.dashboard_routes import dashboard_bp


# Carregar variáveis de ambiente
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados e Flask-Mail
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///prototipo1.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = os.getenv('DEBUG', 'True').lower() in ['true', '1']
    app.config['SECRET_KEY'] = 'chave_super_segura'  # Define manualmente uma chave segura
    
    mail.init_app(app)
    init_db(app)
    '''
    # Registrar Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(funcionario_bp)
    app.register_blueprint(imobiliaria_bp)
    app.register_blueprint(vistoriador_bp)
    app.register_blueprint(dashboard_bp)
    '''
    app.register_blueprint(views_bp)  # Registrando a rota das páginas HTML

    # Configuração do Swagger (Somente no modo debug)
    
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SECRET_KEY'] = 'chave_super_segura'
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # Exemplo: limita tamanho a 5MB
    Session(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
    
