from flask import (
    Blueprint, render_template, request, redirect, url_for,
    jsonify, flash, session
)
from src.models.database import db
from src.utils.auth_utils import login_required, admin_required
import logging

from markupsafe import Markup

# Configuração de logs (útil para depuração e auditoria)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

funcionarios_bp = Blueprint('colaboradores', __name__)

# =====================
# 👥 LISTAGEM DE FUNCIONÁRIOS
# =====================
@funcionarios_bp.route('/', methods=['GET'])
@admin_required
def listar():
    """Exibe a lista de funcionários, com suporte a busca."""
    try:
        # --- Carrega todos os funcionários do JSON ---
        funcionarios = db.listar_usuarios()
        logging.info(f"{len(funcionarios)} funcionários carregados com sucesso.")

        # --- Obtém o usuário atual ---
        usuario_id = session.get('usuario_id')
        usuario = db.obter_usuario(usuario_id)
        admin_check = usuario and usuario.tipo == 'administrador'

        # --- Parâmetro de busca ---
        search = request.args.get('search', '').strip().lower()

        # Remover admin da lista
        funcionarios = [f for f in funcionarios if f.tipo != 'administrador']
        
        # --- Caso tenha busca, filtra ---
        if search:
            funcionarios = [
                f for f in funcionarios
                if search in f.nome.lower()
                or search in str(f.cod_funcionario).lower()
            ]

        
        # Parâmetros de filtro opcionais
        ordenar = request.args.get('ordenar', 'nome')
        direcao = request.args.get('direcao', 'asc')

        # Ordenação
        if ordenar:
            reverse = direcao == 'desc'
            if ordenar == 'cod':
                funcionarios.sort(key=lambda f: f.cod_funcionario, reverse=reverse)
            elif ordenar == 'nome':
                funcionarios.sort(key=lambda f: f.nome, reverse=reverse)
            # elif ordenar == 'data':
            #     funcionarios.sort(key=lambda x: x['data'], reverse=not reverse)  # Mais recente primeiro

        # Pega os parâmetros atuais do link e remove o 'ordenar' e 'direcao' para montar uma nova ordem
        from urllib.parse import urlencode

        args_no_order = request.args.to_dict()
        args_no_order.pop('ordenar', None)
        args_no_order.pop('direcao', None)
        query_string = urlencode(args_no_order)
        

        # --- Paginação ---
        pagina = request.args.get('pagina', 1, type=int)
        # Pega quantos registros mostrar, padrão 5
        funcionarios_por_pagina = request.args.get('funcionarios_por_pagina', 5, type=int)
        total_funcionarios = len(funcionarios)
        inicio = (pagina - 1) * funcionarios_por_pagina
        fim = inicio + funcionarios_por_pagina
        funcionarios_pag = funcionarios[inicio:fim]
        total_paginas = (total_funcionarios + funcionarios_por_pagina - 1) // funcionarios_por_pagina

        # query string atual sem página
        query_params = request.args.to_dict()
        if 'pagina' in query_params:
            del query_params['pagina']

        query_string_pages = '&'.join([f"{k}={v}" for k, v in query_params.items()])

        mostrando_inicio = (pagina - 1) * funcionarios_por_pagina + 1
        mostrando_fim = min(pagina * funcionarios_por_pagina, total_funcionarios)
        total_resultados = total_funcionarios

        return render_template(
            'funcionarios/listar.html',
            usuario=usuario,
            funcionarios=funcionarios_pag,
            admin_check=admin_check,
            search=search,  # mantém o valor no input
            query_string=query_string,
            ordenar=ordenar,
            direcao=direcao,
            query_string_pages=query_string_pages,
            total_paginas=total_paginas,
            pagina=pagina,
            funcionarios_por_pagina=funcionarios_por_pagina,
            mostrando_inicio=mostrando_inicio,
            mostrando_fim=mostrando_fim,
            total_resultados=total_resultados
        )

    except Exception as e:
        logging.exception("Erro ao listar funcionários:")
        flash('Erro ao carregar a lista de funcionários.', 'danger')
        return redirect(url_for('index'))


# =====================
# ➕ ADICIONAR FUNCIONÁRIO
# =====================
@funcionarios_bp.route('/adicionar', methods=['GET', 'POST'])
@admin_required
def adicionar():
    """Adiciona um novo funcionário. Acesso restrito a administradores."""

    usuario=db.obter_usuario(session.get('usuario_id'))
    admin_check = usuario and usuario.tipo == 'administrador'

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        cod_funcionario = request.form.get('cod_funcionario', '').strip()

        if not nome:
            flash('O nome do colaborador é obrigatório.', 'danger')
            return render_template(
                'funcionarios/adicionar.html',
                nome=nome if nome else '',
                email=email if email else '',
                cod_funcionario=cod_funcionario if cod_funcionario else ''
            )
            
        if not email:
            flash('O email do colaborador é obrigatório.', 'danger')
            return render_template(
                'funcionarios/adicionar.html',
                nome=nome if nome else '',
                email=email if email else '',
                cod_funcionario=cod_funcionario if cod_funcionario else ''
            )
            
        if not cod_funcionario:
            flash('O código do colaborador é obrigatório.', 'danger')
            return render_template(
                'funcionarios/adicionar.html',
                nome=nome if nome else '',
                email=email if email else '',
                cod_funcionario=cod_funcionario if cod_funcionario else ''
            )

        try:
            funcionario, message = db.adicionar_usuario(nome=nome, email=email, cod_funcionario=cod_funcionario)
            flash(
                Markup(f'Colaborador <strong>{funcionario.nome}</strong> adicionado com sucesso!'), 'success'
            )
            logging.info(f"Colaborador adicionado: {funcionario.nome} (ID: {funcionario.id})")
            return redirect(url_for('colaboradores.listar'))
        except Exception as e:
            logging.exception("Erro ao adicionar colaborador:")
            flash(
                Markup(f"Erro ao adicionar colaborador: {message}. Tente novamente."), 'danger'
            )

    return render_template(
        'funcionarios/adicionar.html',
        usuario=usuario,
        admin_check=admin_check,
        nome=nome if 'nome' in locals() else '',
        email=email if 'email' in locals() else '',
        cod_funcionario=cod_funcionario if 'cod_funcionario' in locals() else ''
    )


# =====================
# ✏️ EDITAR FUNCIONÁRIO
# =====================
@funcionarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def editar(id):
    """Edita um funcionário existente. Acesso restrito a administradores."""
    funcionario = db.obter_usuario(id)
    if not funcionario:
        flash('Funcionário não encontrado.', 'danger')
        return redirect(url_for('colaboradores.listar'))

    if request.method == 'POST':
        nome = request.form.get('nome_edit', '').strip()
        email = request.form.get('email_edit', '').strip()
        cod_funcionario = request.form.get('cod_funcionario_edit', '').strip()
        novaSenha = request.form.get('novaSenha_edit', '').strip()
        confirmarNovaSenha = request.form.get('confirmarNovaSenha_edit', '').strip()

        # if not nome:
        #     flash('O nome do colaborador é obrigatório.', 'danger')
        #     return redirect(url_for('colaboradores.listar'))
        #     # return render_template('funcionarios/editar.html', funcionario=funcionario)

        # if not email:
        #     flash('O email do colaborador é obrigatório.', 'danger')
        #     return redirect(url_for('colaboradores.listar'))
        #     # return render_template('funcionarios/editar.html', funcionario=funcionario)

        # if not cod_funcionario:
        #     flash('O código do colaborador é obrigatório.', 'danger')
        #     return redirect(url_for('colaboradores.listar'))
        #     # return render_template('funcionarios/editar.html', funcionario=funcionario)
        
        senha = None
        if novaSenha != "" or confirmarNovaSenha != "":
            if not novaSenha:
                flash('Por favor, insira a nova senha.', 'danger')
                return redirect(url_for('colaboradores.listar'))
                # return render_template('funcionarios/editar.html', funcionario=funcionario)
            if not confirmarNovaSenha:
                flash('Por favor, confirme a nova senha.', 'danger')
                return redirect(url_for('colaboradores.listar'))
                # return render_template('funcionarios/editar.html', funcionario=funcionario)
            if novaSenha != confirmarNovaSenha:
                flash('As senhas não coincidem.', 'danger')
                return redirect(url_for('colaboradores.listar'))
                # return render_template('funcionarios/editar.html', funcionario=funcionario)
            senha = novaSenha

        try:
            sucesso, message = db.atualizar_usuario(id=id, nome=nome, email=email, senha=senha, cod_funcionario=cod_funcionario)
            if sucesso:
                flash('Colaborador atualizado com sucesso!', 'success')
                logging.info(f"Colaborador atualizado (ID=%s): novo nome = %s", id, nome)
                return redirect(url_for('colaboradores.listar'))
            else:
                flash(
                    Markup(f"Erro ao atualizar colaborador: {message}"), 'danger'
                )
                return redirect(url_for('colaboradores.listar'))
        except Exception as e:
            logging.exception("Erro ao atualizar colaborador:")
            flash(
                Markup(f"Erro ao atualizar colaborador: {message}"), 'danger'
            )
            return redirect(url_for('colaboradores.listar'))
            
    return redirect(url_for('colaboradores.listar'))
    # return render_template('funcionarios/editar.html', funcionario=funcionario)


# =====================
# 🗑️ REMOVER FUNCIONÁRIO
# =====================
@funcionarios_bp.route('/remover/<int:id>', methods=['POST'])
@admin_required
def remover(id):
    """Remove um funcionário. Acesso restrito a administradores."""

    usuario = db.obter_usuario(id)

    try:
        sucesso = db.remover_usuario(id)
        if sucesso:
            flash(
                Markup(f"Colaborador <strong>{usuario.nome}</strong> removido com sucesso!"), 'success'
            )
            logging.info(f"Colaborador ID={id} removido do sistema.")
        else:
            flash('Erro ao remover colaborador. Verifique se ele está cadastrado.', 'danger')
    except Exception as e:
        logging.exception("Erro ao remover colaborador:")
        flash(f"Erro inesperado ao remover colaborador {usuario.nome}.", 'danger')

    return redirect(url_for('colaboradores.listar'))


# =====================
# 🌐 API (AJAX)
# =====================
@funcionarios_bp.route('/api/listar', methods=['GET'])
@login_required
def api_listar():
    """Retorna a lista de colaboradores em formato JSON."""
    try:
        funcionarios = db.listar_usuarios()
        data = [f.to_dict() for f in funcionarios]
        logging.info(f"API /colaboradores/api/listar retornou {len(data)} registros.")
        return jsonify(data)
    except Exception as e:
        logging.exception("Erro ao obter lista de colaboradores via API:")
        return jsonify({'erro': 'Erro ao obter lista de colaboradores.'}), 500
