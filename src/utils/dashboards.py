import calendar
import locale
from datetime import datetime
from src.models.database import db

locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')


def calcular_horas_por_projeto(usuario_id):
    """Retorna listas de projetos e horas trabalhadas em cada um."""

    registros = obter_dados_dashboard(usuario_id)

    horas_por_projeto = {}
    for registro in registros:
        projeto = db.obter_projeto(registro.projeto_id)
        nome_projeto = projeto.nome if projeto else "Desconhecido"
        horas_por_projeto[nome_projeto] = horas_por_projeto.get(nome_projeto, 0) + registro.horas_trabalhadas

    projetos = list(horas_por_projeto.keys())
    horas = list(horas_por_projeto.values())
    return projetos, horas


def calcular_horas_por_mes(usuario_id):
    """Retorna listas com os últimos 4 meses e suas horas trabalhadas."""

    registros = obter_dados_dashboard(usuario_id)

    horas_por_mes = {}
    for registro in registros:
        if hasattr(registro, "data") and registro.data:
            try:
                # separa mês e ano da string no formato "MM-YYYY"
                mes_str, ano_str = registro.data.split("-")
                mes = int(mes_str)
                ano = int(ano_str)
                chave = (ano, mes)

                horas_por_mes[chave] = horas_por_mes.get(chave, 0) + registro.horas_trabalhadas
            except Exception as e:
                print(f"Erro ao processar data {registro.data}: {e}")

    # Ordenar cronologicamente e pegar os 4 últimos
    horas_por_mes_ordenado = dict(sorted(horas_por_mes.items()))
    ultimos_4 = list(horas_por_mes_ordenado.items())[-4:]

    meses = [
        f"{calendar.month_name[mes][:3].capitalize()}/{ano}"
        for (ano, mes), _ in ultimos_4
    ]
    horas_mensais = [h for _, h in ultimos_4]

    return meses, horas_mensais

def calcular_total_horas_mes(usuario_id):
    """Retorna o total de horas do mês atual.
    - Se admin → soma de todos os funcionários.
    - Se funcionário → soma apenas das próprias horas.
    """
    registros = obter_dados_dashboard(usuario_id)
    agora = datetime.now()
    mes_atual = f"{agora.month:02d}-{agora.year}"

    total_horas_mes = sum(
        registro.horas_trabalhadas
        for registro in registros
        if getattr(registro, "data", "") == mes_atual
    )

    nome_mes_atual = calendar.month_name[agora.month].capitalize()

    return total_horas_mes, nome_mes_atual


def obter_dados_dashboard(usuario_id):
    """Obtém os registros de horas com base no tipo de usuário."""

    usuario = db.obter_usuario(usuario_id)

    # Se for funcionário, mostra só os registros dele
    if usuario and usuario.tipo == 'funcionario':
        registros = db.listar_registros_horas(funcionario_id=usuario.id)
    else:
        registros = db.listar_registros_horas()
    
    return registros