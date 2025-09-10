import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, render_template, redirect, url_for, session
from src.routes.funcionarios import funcionarios_bp
from src.routes.projetos import projetos_bp
from src.routes.registros import registros_bp
from src.routes.auth import auth_bp
from src.utils.auth_utils import login_required
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Chave secreta para sessões

# Registrar blueprints
app.register_blueprint(funcionarios_bp, url_prefix='/funcionarios')
app.register_blueprint(projetos_bp, url_prefix='/projetos')
app.register_blueprint(registros_bp, url_prefix='/registros')
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
@login_required
def index():
    """Página inicial."""
    return render_template('index.html')

@app.route('/home')
def home():
    """Redirecionamento para página inicial ou login."""
    if 'usuario_id' in session:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
