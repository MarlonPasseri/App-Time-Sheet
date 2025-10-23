import pandas as pd
import plotly.express as px
import plotly
import json
from src.models.database import BancoDeDados

class DashboardService:
    def __init__(self):
        self.banco = BancoDeDados()

    def gerar_grafico_horas_por_projeto(self, usuario_id):
        """Gera gráfico de horas trabalhadas por projeto (respeitando o tipo de usuário)."""
        usuario = self.banco.obter_usuario(usuario_id)
        if not usuario:
            return None

        # 🔹 Obter registros com base no tipo de usuário
        if usuario.is_admin():
            registros = self.banco.listar_registros_horas()
        elif usuario.is_funcionario() and usuario.funcionario_id:
            registros = self.banco.listar_registros_horas(funcionario_id=usuario.funcionario_id)
        else:
            return None

        if not registros:
            return None

        # 🔹 Montar DataFrame
        dados = []
        for r in registros:
            projeto = self.banco.obter_projeto(r.projeto_id)
            dados.append({
                "projeto": f"{projeto.id} | {projeto.nome}" if projeto else "Desconhecido",
                "horas": float(r.horas_trabalhadas),
            })

        df = pd.DataFrame(dados)
        df_agrupado = df.groupby("projeto", as_index=False)["horas"].sum()

        # 🔹 Garantir que os tipos são nativos (sem NumPy)
        df_agrupado = df_agrupado.astype({"projeto": str, "horas": float})

        # 🔹 Criar gráfico
        fig = px.bar(
            df_agrupado,
            x="projeto",
            y="horas",
            text="horas",
            title="Horas Trabalhadas por Projeto",
            color="projeto",
        )

        fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig.update_layout(
            xaxis_title="Projeto",
            yaxis_title="Horas Trabalhadas",
            showlegend=False
        )

        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
