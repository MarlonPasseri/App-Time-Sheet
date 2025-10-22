from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.models.database import db
import re

auth_bp = Blueprint('auth', __name__)

# =====================
# 🔐 LOGIN
# =====================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login."""
    if session.get('usuario_id'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '').strip()

        if not all([email, senha]):
            flash('Por favor, preencha todos os campos.', 'danger')
            return render_template('auth/login.html')

        usuario = db.autenticar_usuario(email, senha)
        if usuario:
            session.update({
                'usuario_id': usuario.id,
                'usuario_tipo': usuario.tipo,
                'usuario_nome': usuario.nome
            })
            flash(f'Bem-vindo, {usuario.nome}!', 'success')
            return redirect(url_for('index'))

        flash('Email ou senha incorretos.', 'danger')

    return render_template('auth/login.html')


# =====================
# 🚪 LOGOUT
# =====================
@auth_bp.route('/logout')
def logout():
    """Encerra a sessão do usuário."""
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))


# =====================
# 🧾 REGISTRO
# =====================
@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro de novos usuários."""
    if session.get('usuario_id'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '').strip()
        confirmar_senha = request.form.get('confirmar_senha', '').strip()

        # --- Validações ---
        campos = [nome, email, senha, confirmar_senha]
        if not all(campos):
            flash('Por favor, preencha todos os campos.', 'danger')
            return render_template('auth/registro.html')

        if senha != confirmar_senha:
            flash('As senhas não coincidem.', 'danger')
            return render_template('auth/registro.html')

        if not re.fullmatch(r"[^@]+@geoprojetos\.com\.br", email):
            flash('O email deve ser do domínio @geoprojetos.com.br', 'danger')
            return render_template('auth/registro.html')

        if db.obter_usuario_por_email(email):
            flash('Este email já está em uso.', 'danger')
            return render_template('auth/registro.html')

        # --- Criação do usuário ---
        funcionario = db.adicionar_funcionario(nome)
        usuario, mensagem = db.adicionar_usuario(
            nome=nome,
            email=email,
            senha=senha,
            tipo="funcionario",
            funcionario_id=funcionario.id
        )

        if usuario:
            flash('Conta criada com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('auth.login'))

        flash(f'Erro ao criar conta: {mensagem}', 'danger')

    return render_template('auth/registro.html')


# =====================
# 👤 PERFIL
# =====================
@auth_bp.route('/perfil', methods=['GET', 'POST'])
def perfil():
    """Página de perfil do usuário."""
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('auth.login'))

    usuario = db.obter_usuario(usuario_id)
    if not usuario:
        session.clear()
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        senha_atual = request.form.get('senha_atual', '').strip()
        nova_senha = request.form.get('nova_senha', '').strip()
        confirmar_senha = request.form.get('confirmar_senha', '').strip()

        # --- Atualização de nome ---
        if nome and nome != usuario.nome:
            sucesso, mensagem = db.atualizar_usuario(usuario.id, nome=nome)
            if sucesso:
                session['usuario_nome'] = nome
                flash('Nome atualizado com sucesso!', 'success')
            else:
                flash(f'Erro ao atualizar nome: {mensagem}', 'danger')

        # --- Atualização de senha ---
        if senha_atual or nova_senha or confirmar_senha:
            if not all([senha_atual, nova_senha, confirmar_senha]):
                flash('Preencha todos os campos para alterar a senha.', 'danger')
            elif not usuario.verificar_senha(senha_atual):
                flash('Senha atual incorreta.', 'danger')
            elif nova_senha != confirmar_senha:
                flash('As novas senhas não coincidem.', 'danger')
            else:
                sucesso, mensagem = db.atualizar_usuario(usuario.id, senha=nova_senha)
                if sucesso:
                    flash('Senha atualizada com sucesso!', 'success')
                else:
                    flash(f'Erro ao atualizar senha: {mensagem}', 'danger')

        usuario = db.obter_usuario(usuario_id)

    return render_template('auth/perfil.html', usuario=usuario)

