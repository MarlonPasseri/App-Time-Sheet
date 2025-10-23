import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask, render_template, redirect, url_for, session
from src.routes.funcionarios import funcionarios_bp
from src.routes.projetos import projetos_bp
from src.routes.registros import registros_bp
from src.routes.auth import auth_bp
from src.utils.auth_utils import login_required
from src.utils.dashboards import DashboardService
from src.models.database import db
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

    """Exibe o gráfico de horas na página inicial, respeitando permissões do usuário."""
    usuario_id = session.get('usuario_id')
    usuario = db.obter_usuario(usuario_id)

    # Se for funcionário, mostra só os registros dele
    if usuario and usuario.tipo == 'funcionario' and usuario.funcionario_id:
        registros = db.listar_registros_horas(funcionario_id=usuario.funcionario_id)
    else:
        # Se for admin, mostra todos os registros
        registros = db.listar_registros_horas()

    # --- Gráfico 1: Horas por projeto ---
    horas_por_projeto = {}
    for registro in registros:
        projeto = db.obter_projeto(registro.projeto_id)
        nome_projeto = projeto.nome if projeto else "Desconhecido"
        horas_por_projeto[nome_projeto] = horas_por_projeto.get(nome_projeto, 0) + registro.horas_trabalhadas

    projetos = list(horas_por_projeto.keys())
    horas = list(horas_por_projeto.values())

    # --- Gráfico 2: Horas por mês ---
    import calendar
    import locale
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

    horas_por_mes = {}
    for registro in registros:
        if hasattr(registro, "data") and registro.data:
            try:
                # separa mês e ano da string no formato "MM-YYYY"
                mes_str, ano_str = registro.data.split("-")
                mes = int(mes_str)
                ano = int(ano_str)

                # pega o nome do mês abreviado (ex: "Jan", "Fev", "Mar")
                # nome_mes = f"{calendar.month_name[mes][:3].capitalize()}/{ano}"
                chave = (ano, mes)

                horas_por_mes[chave] = horas_por_mes.get(chave, 0) + registro.horas_trabalhadas
            except Exception as e:
                print(f"Erro ao processar data {registro.data}: {e}")

    # == Ordenar e pegar todos os meses ==
    # meses = list(horas_por_mes.keys())
    # horas_mensais = list(horas_por_mes.values())

    # == Ordenar e pegar últimos 4 meses ==
    horas_por_mes_ordenado = dict(sorted(horas_por_mes.items()))

    # Pega os 4 últimos
    ultimos_4 = list(horas_por_mes_ordenado.items())[-4:]

    # Converte as chaves numéricas (ano, mês) em "NomeMes/Ano" para exibição
    meses = [
        f"{calendar.month_name[mes][:3].capitalize()}/{ano}"
        for (ano, mes), _ in ultimos_4
    ]

    horas_mensais = [h for _, h in ultimos_4]

    # Passar os dados para o template
    return render_template('index.html', projetos=projetos, horas=horas, meses=meses, horas_mensais=horas_mensais)

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
