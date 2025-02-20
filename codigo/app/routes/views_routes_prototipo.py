from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from models import *
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
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

# 🔹 Rota Listagem de Imóveis
@views_bp.route('/imoveis')
def listar_imoveis():
    imoveis = Imovel.query.all()
    return render_template('imoveis.html', imoveis=imoveis)

# 🔹 Rota para Adicionar Imóvel
@views_bp.route('/adicionar_imovel', methods=['GET', 'POST'])
def adicionar_imovel():
    if request.method == 'POST':
        nome = request.form.get("nome_imovel")
        endereco = request.form.get("local")

        if not nome or not endereco:
            flash("Nome e endereço são obrigatórios!", "danger")
            return redirect(url_for("views.adicionar_imovel"))

        novo_imovel = Imovel(
            nome=nome,
            imagem="images/default.jpg",
            endereco=endereco,
            descricao="Imóvel recém-adicionado."
        )
        db.session.add(novo_imovel)
        db.session.commit()

        flash("Imóvel cadastrado com sucesso!", "success")
        return redirect(url_for('views.menu'))

    return render_template('5.adicionarimovel.html')

# 🔹 Rota de Imóvel (com ID dinâmico)
@views_bp.route('/imovel/<int:imovel_id>', methods=['GET'])
def imovel(imovel_id):
    imovel = Imovel.query.get(imovel_id)
    if not imovel:
        flash("Imóvel não encontrado.", "danger")
        return redirect(url_for("views.menu"))

    return render_template('6.imovel.html', imovel=imovel)

# 🔹 Rota do Menu Principal
@views_bp.route('/menu')
def menu():
    imoveis = Imovel.query.all()
    return render_template('3.menu.html', imoveis=imoveis)

# 🔹 Rota de Métricas
@views_bp.route('/metricas')
def metricas():
    return render_template('4.metricas.html')

# 🔹 Rota de Pós-Agendamento
@views_bp.route('/pos_agendamento', methods=['POST', 'GET'])
def pos_agendamento():
    imovel_id = request.form.get("imovel_id")
    data_vistoria = request.form.get("data_vistoria")

    if not imovel_id or not data_vistoria:
        flash("Erro: Imóvel ou data não selecionados.", "danger")
        return redirect(url_for("views.menu"))

    imovel = Imovel.query.get(imovel_id)
    if not imovel:
        flash("Erro: Imóvel não encontrado.", "danger")
        return redirect(url_for("views.menu"))

    # Garantir que a sessão armazene corretamente o imóvel certo
    session["imovel_id"] = imovel.id
    session["imovel_nome"] = imovel.nome
    session["imovel_endereco"] = imovel.endereco
    session["imovel_descricao"] = imovel.descricao
    session["imovel_imagem"] = imovel.imagem
    session["data_vistoria"] = data_vistoria

    return render_template('7.posagendamento.html', imovel=imovel, data_vistoria=data_vistoria)


# 🔹 Outras Rotas

@views_bp.route('/vistoria/<int:imovel_id>', methods=['GET', 'POST'])
def vistoria(imovel_id):
    imovel = Imovel.query.get(imovel_id)
    if not imovel:
        flash("Erro: Imóvel não encontrado.", "danger")
        return redirect(url_for("views.menu"))

    if request.method == "POST":
        # Aqui você pode adicionar lógica para salvar informações da vistoria
        flash("Vistoria realizada com sucesso!", "success")
        return redirect(url_for("views.vistoria_finalizada"))

    return render_template('8.vistoria.html', imovel=imovel)


UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Garante que a pasta de uploads existe
@views_bp.route('/vistoria_finalizada', methods=['POST'])
def vistoria_finalizada():
    imovel_id = session.get("imovel_id")

    if not imovel_id:
        flash("Erro: Nenhum imóvel selecionado.", "danger")
        return redirect(url_for("views.menu"))

    imovel = Imovel.query.get(imovel_id)
    if not imovel:
        flash("Erro: Imóvel não encontrado.", "danger")
        return redirect(url_for("views.menu"))

    # 🔹 Salvando as imagens enviadas e armazenando seus caminhos na sessão
    fotos_salvas = []
    for foto in request.files.getlist("fotos"):
        if foto.filename:
            filename = secure_filename(foto.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            foto.save(file_path)
            fotos_salvas.append(file_path)  # Salva o caminho completo

    session["relatorio_vistoria"] = {
        "Nome do Imóvel": imovel.nome,
        "Data da Vistoria": request.form.get("data_vistoria", "Não informada"),
        "Endereço": imovel.endereco,
        "Título": request.form.get("titulo_vistoria", "Vistoria"),
        "Descrição": request.form.get("descricao_vistoria", "Nenhuma descrição fornecida."),
        "Observações": request.form.get("observacoes", "Nenhuma observação."),
        "Fotos": fotos_salvas  # Agora temos os caminhos corretos das imagens
    }

    flash("Vistoria finalizada com sucesso! Relatório pronto para emissão.", "success")
    return render_template("9.vistoria_finalizada.html")


@views_bp.route('/vistorias_realizadas')
def vistorias_realizadas():
    return render_template('10.vistoriasrealizadas.html')

@views_bp.route('/vistorias_agendadas')
def vistorias_agendadas():
    return render_template('11.vistoriasagendadas.html')

@views_bp.route('/configuracoes')
def configuracoes():
    return render_template('12.configuracoes.html')

@views_bp.route('/editar_cadastro')
def editar_cadastro():
    return render_template('13.editarcadastro.html')

# 🔹 Rota para Editar Imóvel
@views_bp.route('/editar_imovel/<int:imovel_id>', methods=['GET', 'POST'])
def editar_imovel(imovel_id):
    imovel = Imovel.query.get(imovel_id)
    if not imovel:
        flash("Imóvel não encontrado.", "danger")
        return redirect(url_for("views.menu"))

    if request.method == 'POST':
        imovel.nome = request.form.get("nome_imovel")
        imovel.endereco = request.form.get("local")
        db.session.commit()
        flash("Imóvel atualizado com sucesso!", "success")
        return redirect(url_for("views.menu"))
    
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
    imovel = Imovel.query.get(imovel_id) if imovel_id else None
    return render_template('7.2.desejareali.html', imovel=imovel)

@views_bp.route('/emitir_relatorio', methods=['POST'])
def emitir_relatorio():
    """Gera um relatório em PDF com os dados da vistoria e imagens anexadas."""
    
    dados_vistoria = session.get('relatorio_vistoria')

    if not dados_vistoria:
        flash("Erro: Nenhum dado encontrado para gerar o relatório.", "danger")
        return redirect(url_for("views.vistoria_finalizada"))

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