from flask import jsonify
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash
from models import Funcionario
from database import db
import jwt
import datetime
import re
import os
from extensions import mail

# Chave secreta obtida das variáveis de ambiente
SECRET_KEY = os.getenv("SECRET_KEY", "chave_super_secreta")  # Substituir para produção


class AuthService:

    @staticmethod
    def cadastrar(data):
        """
        Cadastra uma nova imobiliária.
        """
        try:
            # Verificar se o e-mail já está cadastrado
            usuario_existente = Funcionario.query.filter_by(email=data["email"]).first()
            if usuario_existente:
                return jsonify({"status": 400, "message": "E-mail já cadastrado."}), 400

            # Criar novo usuário imobiliária
            novo_usuario = Funcionario(
                nome=data["nome"],
                email=data["email"],
                senha=generate_password_hash(data["senha"]),  # Agora a senha é criptografada
                cnpj=data["cnpj"]
            )

            # Adicionar ao banco de dados
            db.session.add(novo_usuario)
            db.session.commit()

            return jsonify({"status": 201, "message": "Imobiliária cadastrada com sucesso!"}), 201

        except Exception as e:
            return jsonify({"status": 500, "message": f"Erro ao cadastrar usuário: {str(e)}"}), 500

    @staticmethod
    def login(data):
        """
        Autentica uma imobiliária.
        """
        credencial = data.get("email") or data.get("cnpj")
        senha = data.get("senha")

        if not credencial or not senha:
            return jsonify({"error": "E-mail ou CNPJ e senha são obrigatórios."}), 400

        # Buscar usuário no banco de dados
        user = Funcionario.query.filter(
            (Funcionario.email == credencial) |
            (Funcionario.cnpj == credencial)
        ).first()

        if not user or not check_password_hash(user.senha, senha):
            return jsonify({"error": "Credenciais inválidas."}), 401

        # Gerar JWT
        token = jwt.encode({
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({"message": "Login bem-sucedido.", "token": token}), 200

    @staticmethod
    def reset_password(token, data):
        """
        Decodifica o token de recuperação e redefine a senha do usuário.
        """
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = decoded["id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado."}), 400
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido."}), 400

        user = Funcionario.query.get(user_id)
        if not user:
            return jsonify({"error": "Usuário não encontrado."}), 404

        new_password = data.get("new_password")
        if not new_password or len(new_password) < 8:
            return jsonify({"error": "A senha deve ter pelo menos 8 caracteres."}), 400

        user.senha = generate_password_hash(new_password)
        db.session.commit()

        return jsonify({"message": "Senha redefinida com sucesso."}), 200

    @staticmethod
    def is_cnpj(numero):
        """
        Verifica se o número fornecido é um CNPJ válido.
        """
        cnpj_pattern = r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$"  # Formato: 00.000.000/0000-00
        return re.match(cnpj_pattern, numero)

    @staticmethod
    def is_creci(numero):
        """
        Verifica se o número fornecido é um CRECI válido.
        """
        creci_pattern = r"^\d{4,7}$"  # Exemplo: 1234567 (4 a 7 dígitos)
        return re.match(creci_pattern, numero)