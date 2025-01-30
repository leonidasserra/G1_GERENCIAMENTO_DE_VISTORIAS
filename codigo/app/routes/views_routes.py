from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Funcionario
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from flask import Response, make_response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import os

views_bp = Blueprint('views', __name__)

# 🔹 Rota de Login
@views_bp.route('/')
@views_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('views.menu'))
    return render_template('1.login.html')

# 🔹 Rota de Cadastro
@views_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('views.login'))
    return render_template('2.cadastro.html')

# 🔹 Rota do Menu Principal
@views_bp.route('/menu')
def menu():
    imoveis = [
        {"id": 1, "nome": "Casa no Calhau", "imagem": "images/casa-calhau.jpg"},
        {"id": 2, "nome": "Apartamento no Vinhais", "imagem": "images/apartamento-vinhais.jpg"}
    ]
    return render_template('3.menu.html', imoveis=imoveis)

# 🔹 Rota de Métricas
@views_bp.route('/metricas')
def metricas():
    return render_template('4.metricas.html')

# 🔹 Rota para Adicionar Imóvel
@views_bp.route('/adicionar_imovel', methods=['GET', 'POST'])
def adicionar_imovel():
    if request.method == 'POST':
        flash('Imóvel cadastrado com sucesso!')
        return redirect(url_for('views.menu'))
    return render_template('5.adicionarimovel.html')

# 🔹 Rota de Imóvel (com ID dinâmico)
@views_bp.route('/imovel/<int:imovel_id>', methods=['GET'])
def imovel(imovel_id):
    imoveis = {
        1: {"id": 1, "nome": "Casa no Calhau", "imagem": "images/casa-calhau.jpg",
            "endereco": "Rua dos Flamingos, 354", "descricao": "Casa espaçosa com 3 quartos e vista para o mar."},
        2: {"id": 2, "nome": "Apartamento no Vinhais", "imagem": "images/apartamento-vinhais.jpg",
            "endereco": "Avenida Central, 200", "descricao": "Apartamento moderno com excelente infraestrutura."}
    }

    imovel = imoveis.get(imovel_id)
    if not imovel:
        flash("Imóvel não encontrado.", "danger")
        return redirect(url_for("views.menu"))

    return render_template('6.imovel.html', imovel=imovel)

# 🔹 Rota de Pós-Agendamento
@views_bp.route('/pos_agendamento', methods=['POST', 'GET'])
def pos_agendamento():
    """Exibe a tela de pós-agendamento após o agendamento da vistoria."""
    
    # Captura os dados do formulário enviados pelo usuário
    imovel_id = request.form.get("imovel_id")
    data_vistoria = request.form.get("data_vistoria")

    if not imovel_id or not data_vistoria:
        flash("Erro: Imóvel ou data não selecionados.", "danger")
        return redirect(url_for("views.menu"))

    # Simulação do banco de dados de imóveis
    imoveis = {
        "1": {"id": 1, "nome": "Casa no Calhau", "imagem": "images/casa-calhau.jpg",
              "endereco": "Rua dos Flamingos, 354", "descricao": "Casa espaçosa com 3 quartos e vista para o mar."},
        "2": {"id": 2, "nome": "Apartamento no Vinhais", "imagem": "images/apartamento-vinhais.jpg",
              "endereco": "Avenida Central, 200", "descricao": "Apartamento moderno com excelente infraestrutura."}
    }

    imovel = imoveis.get(imovel_id)
    if not imovel:
        flash("Erro: Imóvel não encontrado.", "danger")
        return redirect(url_for("views.menu"))

    # Salvar os dados na sessão para serem usados na próxima página
    session["imovel"] = imovel
    session["data_vistoria"] = data_vistoria

    return render_template('7.posagendamento.html', imovel=imovel, data_vistoria=data_vistoria)


# 🔹 Rota para Iniciar a Vistoria
@views_bp.route('/vistoria/<int:imovel_id>', methods=['GET', 'POST'])
def vistoria(imovel_id):
    """Exibe a tela de vistoria do imóvel selecionado após o agendamento."""
    
    # Captura a data da vistoria da sessão
    data_vistoria = session.get("data_vistoria", "Não informada")

    # Recupera os dados do imóvel da sessão
    imovel = session.get("imovel", {})

    if not imovel or imovel.get("id") != imovel_id:
        flash("Erro: Nenhum imóvel selecionado ou ID inválido.", "danger")
        return redirect(url_for("views.menu"))

    return render_template("8.vistoria.html", imovel=imovel, data_vistoria=data_vistoria)


# 🔹 Rota para Finalizar a Vistoria
import os
from werkzeug.utils import secure_filename

@views_bp.route('/vistoria_finalizada', methods=['POST'])
def vistoria_finalizada():
    """Finaliza a vistoria e armazena os dados preenchidos na sessão."""

    titulo = request.form.get("titulo")
    descricao = request.form.get("descricao")
    observacoes = request.form.get("observacoes")
    fotos = request.files.getlist("fotos")

    if not titulo or not descricao:
        flash("Erro: O título e a descrição são obrigatórios!", "danger")
        return redirect(url_for("views.vistoria", imovel_id=session.get("imovel", {}).get("id")))

    # Criar pasta de uploads se não existir
    upload_folder = "static/uploads"
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Salvar informações na sessão
    session["relatorio_vistoria"] = {
        "Nome do Imóvel": session.get("imovel", {}).get("nome", "Não informado"),
        "Data da Vistoria": session.get("data_vistoria", "Não informada"),
        "Endereço": session.get("imovel", {}).get("endereco", "Não informado"),
        "Título": titulo,
        "Descrição": descricao,
        "Observações": observacoes,
        "Fotos": [],
    }

    # Salvando imagens corretamente
    for foto in fotos:
        if foto and foto.filename != "":
            from werkzeug.utils import secure_filename
            filename = secure_filename(foto.filename)
            caminho_foto = os.path.join(upload_folder, filename)
            foto.save(caminho_foto)
            session["relatorio_vistoria"]["Fotos"].append(caminho_foto)

    return redirect(url_for("views.vistoria_finalizada_template"))



@views_bp.route('/vistoria_finalizada_template')
def vistoria_finalizada_template():
    """Renderiza a página de vistoria finalizada"""
    return render_template('9.vistoria_finalizada.html')


# 🔹 Relatórios e Configurações
@views_bp.route('/vistoriasrealizadas')
def vistorias_realizadas():
    return render_template('10.vistoriasrealizadas.html')

@views_bp.route('/vistoriasagendadas')
def vistorias_agendadas():
    return render_template('11.vistoriasagendadas.html')

@views_bp.route('/configuracoes')
def configuracoes():
    return render_template('12.configuracoes.html')

@views_bp.route('/editarcadastro')
def editar_cadastro():
    return render_template('13.editarcadastro.html')

@views_bp.route('/editarimovel/<int:imovel_id>', methods=['GET'])
def editar_imovel(imovel_id):
    """Carrega os dados do imóvel para edição."""

    # Simulação de um banco de dados de imóveis
    imoveis = {
        1: {"id": 1, "nome": "Casa no Calhau", "imagem": "images/casa-calhau.jpg",
            "endereco": "Rua dos Flamingos, 354", "descricao": "Casa espaçosa com 3 quartos."},
        2: {"id": 2, "nome": "Apartamento no Vinhais", "imagem": "images/apartamento-vinhais.jpg",
            "endereco": "Avenida Central, 200", "descricao": "Apartamento moderno e bem localizado."}
    }

    # Busca o imóvel pelo ID
    imovel = imoveis.get(imovel_id)

    # Se o imóvel não existir, redireciona para o menu com um alerta
    if not imovel:
        flash("Erro: Imóvel não encontrado.", "danger")
        return redirect(url_for("views.menu"))

    # Renderiza a página com os dados do imóvel
    return render_template('14.editarimovel.html', imovel=imovel)


@views_bp.route('/deseja_desativar')
def deseja_desativar():
    return render_template('14.1.desejadesativ.html')

@views_bp.route('/deseja_reagendar')
def deseja_reagendar():
    return render_template('7.1.desejareag.html')

@views_bp.route('/deseja_realizar')
def deseja_realizar():
    imovel_id = request.args.get('imovel_id')
    return render_template('7.2.desejareali.html', imovel_id=imovel_id)

@views_bp.route('/emitir_relatorio', methods=['POST'])
def emitir_relatorio():
    """Gera um relatório em PDF com os dados da vistoria e imagens anexadas, formatadas corretamente."""

    dados_vistoria = session.get('relatorio_vistoria', {})

    if not dados_vistoria:
        return "Erro: Nenhum dado encontrado para gerar o relatório.", 400

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    page_width, page_height = letter

    # Configuração inicial
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, page_height - 50, "Relatório de Vistoria")

    p.setFont("Helvetica", 12)
    y_position = page_height - 90  # Ajustando a posição inicial abaixo do cabeçalho
    line_height = 20  # Espaçamento entre as linhas

    # Exibir todas as informações textuais antes dos anexos
    campos_a_exibir = ["Nome do Imóvel", "Data da Vistoria", "Endereço", "Título", "Descrição", "Observações"]
    
    for campo in campos_a_exibir:
        valor = dados_vistoria.get(campo, "Não informado")
        p.drawString(100, y_position, f"{campo}: {valor}")
        y_position -= line_height

        # Se a posição estiver muito baixa, cria uma nova página
        if y_position < 100:
            p.showPage()
            p.setFont("Helvetica", 12)
            y_position = page_height - 50

    # Adicionar um espaço antes dos anexos
    y_position -= 40
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y_position, "Anexos:")

    # Ajuste para garantir que as imagens fiquem bem posicionadas
    y_position -= 30
    p.setFont("Helvetica", 12)

    fotos = dados_vistoria.get("Fotos", [])
    for foto in fotos:
        if os.path.exists(foto):
            # Se não houver espaço suficiente, cria uma nova página
            if y_position < 200:
                p.showPage()
                p.setFont("Helvetica-Bold", 14)
                p.drawString(100, page_height - 50, "Anexos:")
                y_position = page_height - 100  # Redefine a posição inicial da imagem

            # Definir tamanho fixo para as imagens
            img_width, img_height = 250, 180
            p.drawImage(foto, 100, y_position - img_height, width=img_width, height=img_height)

            # Ajustar a posição para a próxima imagem
            y_position -= img_height + 30  # Espaçamento entre as imagens

    # Finaliza o documento
    p.save()
    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=relatorio_vistoria.pdf'

    return response

