from functools import wraps
from flask import session, redirect, url_for, flash, request

def login_required(f):
    """Decorator para verificar se o usuário está logado."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'danger')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator para verificar se o usuário é administrador."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'danger')
            return redirect(url_for('auth.login', next=request.url))
        
        if session.get('usuario_tipo') != 'administrador':
            flash('Acesso restrito a administradores.', 'danger')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function
