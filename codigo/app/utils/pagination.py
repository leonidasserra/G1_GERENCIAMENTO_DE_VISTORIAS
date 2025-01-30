def paginate(query, params):
    """
    Pagina os resultados de uma consulta SQLAlchemy.

    :param query: Objeto de consulta SQLAlchemy.
    :param params: Dicionário com os parâmetros 'page' e 'limit'.
    :return: Um dicionário contendo os resultados paginados.
    """
    page = int(params.get('page', 1))
    limit = int(params.get('limit', 10))

    if page <= 0 or limit <= 0:
        raise ValueError("Os parâmetros 'page' e 'limit' devem ser maiores que zero.")

    total_items = query.count()  # Conta o total de itens na consulta
    total_pages = (total_items + limit - 1) // limit
    offset = (page - 1) * limit

    items = query.offset(offset).limit(limit).all()  # Aplica a paginação na consulta

    return {
        "page": page,
        "total_pages": total_pages,
        "total_items": total_items,
        "items": [item.to_dict() for item in items],  # Serializa os objetos para JSON
    }
