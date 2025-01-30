from app import create_app
from database import db
from models import Funcionario

app = create_app()
with app.app_context():
    Funcionario.query.filter(Funcionario.senha == "senha123").delete()
    db.session.commit()
    print("Usuários com senha em texto puro foram removidos.")

with app.app_context():
    db.drop_all()  # Apaga todas as tabelas
    db.create_all()  # Cria as tabelas novamente
    print("Banco de dados atualizado!")    