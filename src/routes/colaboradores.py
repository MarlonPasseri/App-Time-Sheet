from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session
from src.models.database import db
from src.utils.auth_utils import login_required, admin_required

colaboradores_bp = Blueprint('colaboradores', __name__)

@colaboradores_bp.route('/')
@admin_required
def listar():
    """Exibe a lista de colaboradores. Acesso restrito a administradores."""
    funcionarios = db.listar_funcionarios()
    return render_template('colaboradores/listar.html', funcionarios=funcionarios)

@colaboradores_bp.route('/adicionar', methods=['GET', 'POST'])
@admin_required
def adicionar():
    """Adiciona um novo colaborador. Acesso restrito a administradores."""
    if request.method == 'POST':
        nome = request.form.get('nome')
        if nome:
            funcionario = db.adicionar_funcionario(nome)
            flash('Colaborador adicionado com sucesso!', 'success')
            return redirect(url_for('colaboradores.listar'))
        else:
            flash('Nome do colaborador é obrigatório!', 'danger')
    
    return render_template('colaboradores/adicionar.html')

@colaboradores_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def editar(id):
    """Edita um colaborador existente. Acesso restrito a administradores."""
    funcionario = db.obter_funcionario(id)
    if not funcionario:
        flash('Colaborador não encontrado!', 'danger')
        return redirect(url_for('colaboradores.listar'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        if nome:
            db.atualizar_funcionario(id, nome)
            flash('Colaborador atualizado com sucesso!', 'success')
            return redirect(url_for('colaboradores.listar'))
        else:
            flash('Nome do colaborador é obrigatório!', 'danger')
    
    return render_template('colaboradores/editar.html', funcionario=funcionario)

@colaboradores_bp.route('/remover/<int:id>', methods=['POST'])
def remover(id):
    """Remove um colaborador."""
    if db.remover_funcionario(id):
        flash('Colaborador removido com sucesso!', 'success')
    else:
        flash('Erro ao remover colaborador!', 'danger')
    
    return redirect(url_for('colaboradores.listar'))

# API para uso em AJAX
@colaboradores_bp.route('/api/listar', methods=['GET'])
def api_listar():
    """Retorna a lista de colaboradores em formato JSON."""
    funcionarios = db.listar_funcionarios()
    return jsonify([f.to_dict() for f in funcionarios])
