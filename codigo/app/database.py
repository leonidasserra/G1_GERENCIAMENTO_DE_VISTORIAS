from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados
