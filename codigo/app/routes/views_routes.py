from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Funcionario  # Importa o modelo atualizado
from werkzeug.security import check_password_hash
from flask import Response, make_response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

views_bp = Blueprint('views', __name__)

@views_bp.route('/')
@views_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cnpj = request.form.get('cnpj')  # Captura o CNPJ inserido
        senha = request.form.get('senha')  # Captura a senha inserida

        print(f"Tentativa de login - CNPJ: {cnpj}, Senha: {senha}")  # Log para depuração

        return redirect(url_for('views.menu'))  # Redireciona sempre para o menu

    return render_template('1.login.html')

@views_bp.route('/menu')
def menu():
    """Renderiza a página do menu com a lista de imóveis."""

    # Simulação de imóveis cadastrados no banco
    imoveis = [
        {"id": 1, "nome": "Casa no Calhau", "imagem": "images/casa-calhau.jpg"},
        {"id": 2, "nome": "Apartamento no Vinhais", "imagem": "images/apartamento-vinhais.jpg"}
    ]

    return render_template('3.menu.html', imoveis=imoveis)

@views_bp.route('/logout')
def logout():
    """Remove o usuário da sessão e redireciona para a página de login."""
    session.pop('user_id', None)
    return redirect(url_for('views.login'))

@views_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """Renderiza a página de cadastro e processa o formulário."""
    if request.method == 'POST':
        nome = request.form.get('nome')
        cnpj = request.form.get('cnpj')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')

        if senha != confirmar_senha:
            flash('As senhas não coincidem!')
            return redirect(url_for('views.cadastro'))

        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('views.login'))

    return render_template('2.cadastro.html')

@views_bp.route('/metricas')
def metricas():
    return render_template('4.metricas.html')

@views_bp.route('/adicionar_imovel', methods=['GET', 'POST'])
def adicionar_imovel():
    """Renderiza a página de adição de imóvel."""
    if request.method == 'POST':
        flash('Imóvel cadastrado com sucesso!')
        return redirect(url_for('views.menu'))

    return render_template('5.adicionarimovel.html')

@views_bp.route('/imovel/<int:imovel_id>', methods=['GET'])
def imovel(imovel_id):
    # Simulação de um banco de dados de imóveis
    imoveis = {
        1: {"id": 1, "nome": "Casa no Calhau", "imagem": "images/pexels-binyaminmellish-1396122.jpg",
            "endereco": "Rua dos Flamingos, 354", "descricao": "Casa espaçosa com 3 quartos e vista para o mar."},
        2: {"id": 2, "nome": "Apartamento no Vinhais", "imagem": "images/vinhais.jpg",
            "endereco": "Avenida Central, 200", "descricao": "Apartamento moderno com excelente infraestrutura."}
    }

    imovel = imoveis.get(imovel_id)  # Obtém o imóvel pelo ID
    if not imovel:
        flash("Imóvel não encontrado.", "danger")
        return redirect(url_for("views.menu"))

    return render_template('6.imovel.html', imovel=imovel)

@views_bp.route('/agendar_vistoria', methods=['POST'])
def agendar_vistoria():
    """Processa o agendamento da vistoria e redireciona para a tela de pós-agendamento."""

    imovel_id = request.form.get("imovel_id")
    data_vistoria = request.form.get("data_vistoria")  # Captura a data selecionada

    if not imovel_id or not data_vistoria:
        flash("Erro: Nenhum imóvel ou data selecionados.", "danger")
        return redirect(url_for("views.menu"))

    try:
        imovel_id = int(imovel_id)  # Converte ID para número inteiro
    except ValueError:
        flash("Erro: ID do imóvel inválido.", "danger")
        return redirect(url_for("views.menu"))

    # Salva os dados na sessão
    session["imovel_id"] = imovel_id
    session["data_vistoria"] = data_vistoria  # Salva a data escolhida

    # Redireciona para a tela de pós-agendamento
    return redirect(url_for("views.pos_agendamento"))

@views_bp.route('/posagendamento', methods=['POST'])
def pos_agendamento():
    imovel_id = request.form.get("imovel_id")
    data_vistoria = request.form.get("data_vistoria")

    if not imovel_id or not data_vistoria:
        flash("Erro: Imóvel ou data da vistoria não foram informados.", "danger")
        return redirect(url_for("views.menu"))

    try:
        imovel_id = int(imovel_id)
    except ValueError:
        flash("Erro: ID do imóvel inválido.", "danger")
        return redirect(url_for("views.menu"))

    # Simulação do banco de dados de imóveis
    imoveis = {
        1: {"id": 1, "nome": "Casa no Calhau", "imagem": "images/pexels-binyaminmellish-1396122.jpg",
            "endereco": "Rua dos Flamingos, 354", "descricao": "Casa espaçosa com 3 quartos e vista para o mar."},
        2: {"id": 2, "nome": "Apartamento no Vinhais", "imagem": "images/vinhais.jpg",
            "endereco": "Avenida Central, 200", "descricao": "Apartamento moderno com excelente infraestrutura."}
    }

    imovel = imoveis.get(imovel_id)
    if not imovel:
        flash("Erro: Imóvel não encontrado.", "danger")
        return redirect(url_for("views.menu"))

    session["imovel"] = imovel
    session["data_vistoria"] = data_vistoria  # Salva a data da vistoria na sessão

    return render_template('7.posagendamento.html', imovel=imovel, data_vistoria=data_vistoria)



@views_bp.route('/vistoria', methods=['GET', 'POST'])
def vistoria():
    """Processa o agendamento de vistoria e exibe a página de vistoria."""

    # Verifica se há um imóvel na sessão
    imovel = session.get("imovel")
    data_vistoria = session.get("data_vistoria")

    if not imovel or not data_vistoria:
        flash("Erro: Nenhum imóvel ou data da vistoria encontrados.", "danger")
        return redirect(url_for("views.menu"))

    return render_template("8.vistoria.html", imovel=imovel, data_vistoria=data_vistoria)


@views_bp.route('/vistoria_finalizada', methods=['GET', 'POST'])
def vistoria_finalizada():
    """Armazena os dados da vistoria na sessão e exibe a página final."""

    if request.method == 'POST':
        session['relatorio_vistoria'] = {
            "Título": request.form.get('titulo', 'N/A'),
            "Descrição": request.form.get('descricao', 'N/A'),
            "Observações": request.form.get('observacoes', 'N/A'),
        }

    return render_template('9.vistoria_finalizada.html')

@views_bp.route('/emitir_relatorio', methods=['POST'])
def emitir_relatorio():
    """Gera um PDF com os dados da vistoria."""

    dados_vistoria = session.get('relatorio_vistoria', {})

    if not dados_vistoria:
        return "Erro: Nenhum dado encontrado para gerar o relatório.", 400

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 750, "Relatório de Vistoria")

    p.setFont("Helvetica", 12)
    y_position = 700

    # Adicionando informações da vistoria
    for chave, valor in dados_vistoria.items():
        p.drawString(100, y_position, f"{chave}: {valor}")
        y_position -= 30

    p.save()
    buffer.seek(0)
    
    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=relatorio_vistoria.pdf'
    
    return response
