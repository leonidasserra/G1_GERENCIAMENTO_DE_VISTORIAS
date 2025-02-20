from flask import request, jsonify
import jwt
from functools import wraps

SECRET_KEY = "tomb69Charp"  # Certifique-se de usar uma chave forte

def autorizacao_permitida(tipos_permitidos):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return jsonify({"error": "Token não fornecido."}), 401
            try:
                decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                if decoded["tipo"] not in tipos_permitidos:
                    return jsonify({"error": "Acesso não autorizado."}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expirado."}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Token inválido."}), 401
            return f(*args, **kwargs)
        return wrapper
    return decorator
