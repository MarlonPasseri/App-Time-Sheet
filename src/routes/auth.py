from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.models.database import db
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login."""
    # Se o usuário já está logado, redireciona para a página inicial
    if 'usuario_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        if not email or not senha:
            flash('Por favor, preencha todos os campos.', 'danger')
            return render_template('auth/login.html')
        
        # Tenta autenticar o usuário
        usuario = db.autenticar_usuario(email, senha)
        
        if usuario:
            # Armazena o ID do usuário na sessão
            session['usuario_id'] = usuario.id
            session['usuario_tipo'] = usuario.tipo
            session['usuario_nome'] = usuario.nome
            
            flash(f'Bem-vindo, {usuario.nome}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email ou senha incorretos.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """Encerra a sessão do usuário."""
    session.pop('usuario_id', None)
    session.pop('usuario_tipo', None)
    session.pop('usuario_nome', None)
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro de novos usuários."""
    # Se o usuário já está logado, redireciona para a página inicial
    if 'usuario_id' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        # Validações básicas
        if not nome or not email or not senha or not confirmar_senha:
            flash('Por favor, preencha todos os campos.', 'danger')
            return render_template('auth/registro.html')
        
        if senha != confirmar_senha:
            flash('As senhas não coincidem.', 'danger')
            return render_template('auth/registro.html')
        
        # Validar email empresarial
        if not re.match(r"[^@]+@geoprojetos\.com\.br$", email):
            flash('O email deve ser do domínio @geoprojetos.com.br', 'danger')
            return render_template('auth/registro.html')
        
        # Verificar se o email já está em uso
        if db.obter_usuario_por_email(email):
            flash('Este email já está em uso.', 'danger')
            return render_template('auth/registro.html')
        
        # Criar um novo funcionário para o usuário
        funcionario = db.adicionar_funcionario(nome)
        
        # Criar o usuário associado ao funcionário
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
        else:
            flash(f'Erro ao criar conta: {mensagem}', 'danger')
    
    return render_template('auth/registro.html')

@auth_bp.route('/perfil', methods=['GET', 'POST'])
def perfil():
    """Página de perfil do usuário."""
    # Verifica se o usuário está logado
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para acessar esta página.', 'danger')
        return redirect(url_for('auth.login'))
    
    usuario = db.obter_usuario(session['usuario_id'])
    if not usuario:
        session.clear()
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha_atual = request.form.get('senha_atual')
        nova_senha = request.form.get('nova_senha')
        confirmar_senha = request.form.get('confirmar_senha')
        
        # Atualizar nome
        if nome and nome != usuario.nome:
            sucesso, mensagem = db.atualizar_usuario(usuario.id, nome=nome)
            if sucesso:
                session['usuario_nome'] = nome
                flash('Nome atualizado com sucesso!', 'success')
            else:
                flash(f'Erro ao atualizar nome: {mensagem}', 'danger')
        
        # Atualizar senha
        if senha_atual and nova_senha and confirmar_senha:
            if not usuario.verificar_senha(senha_atual):
                flash('Senha atual incorreta.', 'danger')
            elif nova_senha != confirmar_senha:
                flash('As novas senhas não coincidem.', 'danger')
            else:
                sucesso, mensagem = db.atualizar_usuario(usuario.id, senha=nova_senha)
                if sucesso:
                    flash('Senha atualizada com sucesso!', 'success')
                else:
                    flash(f'Erro ao atualizar senha: {mensagem}', 'danger')
        
        # Recarregar o usuário após as atualizações
        usuario = db.obter_usuario(session['usuario_id'])
    
    return render_template('auth/perfil.html', usuario=usuario)
