import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, render_template, redirect, url_for, session
from src.routes.funcionarios import funcionarios_bp
from src.routes.projetos import projetos_bp
from src.routes.registros import registros_bp
from src.routes.auth import auth_bp
from src.utils.auth_utils import login_required
from src.utils.dashboards import *
from src.models.database import db
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Chave secreta para sessões

# Registrar blueprints
app.register_blueprint(funcionarios_bp, url_prefix='/colaboradores')
app.register_blueprint(projetos_bp, url_prefix='/contratos')
app.register_blueprint(registros_bp, url_prefix='/registros')
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
@login_required
def index():
    """Página inicial com gráficos de horas."""

    usuario_id = session.get('usuario_id')

    projetos, horas = calcular_horas_por_projeto(usuario_id)
    meses, horas_mensais = calcular_horas_por_mes(usuario_id)
    total_horas_regis, nome_mes_atual = calcular_total_horas_mes(usuario_id)

    usuario = db.obter_usuario(usuario_id)
    admin_check = session.get('usuario_tipo') == 'administrador'

    avisos = db.listar_avisos()
    total_horas_mes_atual = db.obter_horas_mes_atual()

    # Passar os dados para o template
    return render_template(
        'index.html',
        projetos=projetos, 
        horas=horas, meses=meses, 
        horas_mensais=horas_mensais, 
        total_horas_regis=total_horas_regis, 
        nome_mes_atual=nome_mes_atual, 
        usuario=usuario, 
        admin_check=admin_check,
        avisos=avisos,
        total_horas_mes_atual=total_horas_mes_atual
    )

@app.route('/home')
def home():
    """Redirecionamento para página inicial ou login."""
    
    if 'usuario_id' in session:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('auth.login'))

@app.template_filter('formatar_horas')
def formatar_horas(horas):
    if horas is None:
        return "0h"
    horas_inteiras = int(horas)
    minutos = int(round((horas - horas_inteiras) * 60))
    return f"{horas_inteiras}h {f'{minutos}min' if minutos else ''}"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
