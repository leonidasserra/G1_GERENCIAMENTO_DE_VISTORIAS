'''
import psycopg2

try:
    conn = psycopg2.connect(
        dbname="prototipo1",
        user="usuario_vistoria",
        password="1234",
        host="localhost",
        port="5432"
    )
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"Erro ao conectar ao banco: {e}")

from app import create_app
from database import db
from models import Funcionario

app = create_app()  # Cria a aplicação Flask

with app.app_context():  # Garante que estamos dentro do contexto da aplicação
    usuarios = Funcionario.query.all()

    for user in usuarios:
        print(f"ID: {user.id}, Nome: {user.nome}, CNPJ: {user.cnpj}, Senha Hash: {user.senha_hash}")
'''