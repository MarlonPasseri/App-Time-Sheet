from flask import (
    Blueprint, render_template, request, redirect, url_for,
    jsonify, flash, session
)
from src.models.database import db
from src.utils.auth_utils import login_required, admin_required
import logging

# Configuração de logs (útil para depuração e auditoria)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

funcionarios_bp = Blueprint('colaboradores', __name__)

# =====================
# 👥 LISTAGEM DE FUNCIONÁRIOS
# =====================
@funcionarios_bp.route('/')
@admin_required
def listar():
    """Exibe a lista de funcionários. Acesso restrito a administradores."""
    try:
        funcionarios = db.listar_funcionarios()
        logging.info(f"{len(funcionarios)} funcionários carregados com sucesso.")
        return render_template('funcionarios/listar.html', funcionarios=funcionarios)
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
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()

        if not nome:
            flash('O nome do funcionário é obrigatório.', 'danger')
            return render_template('funcionarios/adicionar.html')

        try:
            funcionario = db.adicionar_funcionario(nome)
            flash(f'Funcionário "{funcionario.nome}" adicionado com sucesso!', 'success')
            logging.info(f"Funcionário adicionado: {funcionario.nome} (ID: {funcionario.id})")
            return redirect(url_for('colaboradores.listar'))
        except Exception as e:
            logging.exception("Erro ao adicionar funcionário:")
            flash('Erro ao adicionar funcionário. Tente novamente.', 'danger')

    return render_template('funcionarios/adicionar.html')


# =====================
# ✏️ EDITAR FUNCIONÁRIO
# =====================
@funcionarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def editar(id):
    """Edita um funcionário existente. Acesso restrito a administradores."""
    funcionario = db.obter_funcionario(id)
    if not funcionario:
        flash('Funcionário não encontrado.', 'danger')
        return redirect(url_for('colaboradores.listar'))

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()

        if not nome:
            flash('O nome do funcionário é obrigatório.', 'danger')
            return render_template('funcionarios/editar.html', funcionario=funcionario)

        try:
            sucesso = db.atualizar_funcionario(id, nome)
            if sucesso:
                flash('Funcionário atualizado com sucesso!', 'success')
                logging.info(f"Funcionário atualizado (ID=%s): novo nome = %s", id, nome)
                return redirect(url_for('colaboradores.listar'))
            else:
                flash('Erro ao atualizar funcionário.', 'danger')
        except Exception as e:
            logging.exception("Erro ao atualizar funcionário:")
            flash('Erro inesperado ao atualizar funcionário.', 'danger')

    return render_template('funcionarios/editar.html', funcionario=funcionario)


# =====================
# 🗑️ REMOVER FUNCIONÁRIO
# =====================
@funcionarios_bp.route('/remover/<int:id>', methods=['POST'])
@admin_required
def remover(id):
    """Remove um funcionário. Acesso restrito a administradores."""
    try:
        sucesso = db.remover_funcionario(id)
        if sucesso:
            flash('Funcionário removido com sucesso!', 'success')
            logging.info(f"Funcionário ID={id} removido do sistema.")
        else:
            flash('Erro ao remover funcionário. Verifique se ele está vinculado a um usuário ou projeto.', 'danger')
    except Exception as e:
        logging.exception("Erro ao remover funcionário:")
        flash('Erro inesperado ao remover funcionário.', 'danger')

    return redirect(url_for('colaboradores.listar'))


# =====================
# 🌐 API (AJAX)
# =====================
@funcionarios_bp.route('/api/listar', methods=['GET'])
@login_required
def api_listar():
    """Retorna a lista de funcionários em formato JSON."""
    try:
        funcionarios = db.listar_funcionarios()
        data = [f.to_dict() for f in funcionarios]
        logging.info(f"API /colaboradores/api/listar retornou {len(data)} registros.")
        return jsonify(data)
    except Exception as e:
        logging.exception("Erro ao obter lista de funcionários via API:")
        return jsonify({'erro': 'Erro ao obter lista de funcionários.'}), 500
