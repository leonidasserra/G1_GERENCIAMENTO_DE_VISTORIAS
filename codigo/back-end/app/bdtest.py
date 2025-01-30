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
