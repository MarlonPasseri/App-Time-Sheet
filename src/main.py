import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, render_template, redirect, url_for, session
from src.routes.colaboradores import colaboradores_bp
from src.routes.contratos import contratos_bp
from src.routes.registros import registros_bp
from src.routes.auth import auth_bp
from src.utils.auth_utils import login_required
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Chave secreta para sessões

# Formatação da hora
@app.template_filter('formatar_horas')
def formatar_horas(horas_float: float) -> str:
    horas = int(horas_float)
    decimal = horas_float % 1
    minutos = int(decimal * 60)

    if minutos == 0:
        return f"{horas} hora{'s' if horas != 1 else ''}"
    else:
        return f"{horas} hora{'s' if horas != 1 else ''} e {minutos} minutos"

# Registrar blueprints
app.register_blueprint(colaboradores_bp, url_prefix='/colaboradores')
app.register_blueprint(contratos_bp, url_prefix='/contratos')
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
