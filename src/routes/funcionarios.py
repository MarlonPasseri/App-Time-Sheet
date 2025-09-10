from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session
from src.models.database import db
from src.utils.auth_utils import login_required, admin_required

funcionarios_bp = Blueprint('funcionarios', __name__)

@funcionarios_bp.route('/')
@admin_required
def listar():
    """Exibe a lista de funcionários. Acesso restrito a administradores."""
    funcionarios = db.listar_funcionarios()
    return render_template('funcionarios/listar.html', funcionarios=funcionarios)

@funcionarios_bp.route('/adicionar', methods=['GET', 'POST'])
@admin_required
def adicionar():
    """Adiciona um novo funcionário. Acesso restrito a administradores."""
    if request.method == 'POST':
        nome = request.form.get('nome')
        if nome:
            funcionario = db.adicionar_funcionario(nome)
            flash('Funcionário adicionado com sucesso!', 'success')
            return redirect(url_for('funcionarios.listar'))
        else:
            flash('Nome do funcionário é obrigatório!', 'danger')
    
    return render_template('funcionarios/adicionar.html')

@funcionarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def editar(id):
    """Edita um funcionário existente. Acesso restrito a administradores."""
    funcionario = db.obter_funcionario(id)
    if not funcionario:
        flash('Funcionário não encontrado!', 'danger')
        return redirect(url_for('funcionarios.listar'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        if nome:
            db.atualizar_funcionario(id, nome)
            flash('Funcionário atualizado com sucesso!', 'success')
            return redirect(url_for('funcionarios.listar'))
        else:
            flash('Nome do funcionário é obrigatório!', 'danger')
    
    return render_template('funcionarios/editar.html', funcionario=funcionario)

@funcionarios_bp.route('/remover/<int:id>', methods=['POST'])
def remover(id):
    """Remove um funcionário."""
    if db.remover_funcionario(id):
        flash('Funcionário removido com sucesso!', 'success')
    else:
        flash('Erro ao remover funcionário!', 'danger')
    
    return redirect(url_for('funcionarios.listar'))

# API para uso em AJAX
@funcionarios_bp.route('/api/listar', methods=['GET'])
def api_listar():
    """Retorna a lista de funcionários em formato JSON."""
    funcionarios = db.listar_funcionarios()
    return jsonify([f.to_dict() for f in funcionarios])
