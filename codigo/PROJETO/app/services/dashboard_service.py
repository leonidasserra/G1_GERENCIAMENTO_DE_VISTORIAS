from models import Vistoria

class DashboardService:
    @staticmethod
    def listar_vistorias(params):
        # Parâmetros de paginação
        pagina = int(params.get("pagina", 1))
        limite = int(params.get("limite", 10))
        offset = (pagina - 1) * limite

        # Consulta ao banco de dados com paginação
        vistorias = Vistoria.query.offset(offset).limit(limite).all()
        total = Vistoria.query.count()

        # Formatar a resposta
        return {
            "pagina": pagina,
            "limite": limite,
            "total_vistorias": total,
            "vistorias": [v.to_dict() for v in vistorias]  # Implementar método `to_dict` no modelo
        }, 200
