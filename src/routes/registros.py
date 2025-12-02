from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, send_file, session
from src.models.database import db
from src.utils.auth_utils import login_required, admin_required
from src.utils.relatorio_personalizado import adaptar_exportacao_relatorio_mensal
from datetime import datetime
import pandas as pd
import os
import tempfile

registros_bp = Blueprint('registros', __name__)

@registros_bp.route('/', methods=['GET'])
@login_required
def listar():
    """Exibe a lista de registros de horas com base nas permissões do usuário."""

    # Obtém o usuário atual
    usuario_id = session.get('usuario_id')
    usuario = db.obter_usuario(usuario_id)
    admin_check = usuario and usuario.tipo == 'administrador'
    
    # Parâmetros de filtro opcionais
    projeto_id = request.args.get('projeto_id_filter', type=int)
    mes_ano = request.args.get('mes_ano_filter')
    ordenar = request.args.get('ordenar', 'id')
    direcao = request.args.get('direcao', 'asc')

    # Se funcionário, força o próprio ID
    if admin_check:
        funcionario_id = request.args.get('funcionario_id_filter', type=int)
    else:
        funcionario_id = usuario.id

    # Obtém os registros filtrados
    registros = db.listar_registros_horas(
        funcionario_id=funcionario_id,
        projeto_id=projeto_id,
        mes_ano=mes_ano
    )
    
    # Obtém listas de funcionários e projetos para os filtros
    funcionarios = db.listar_usuarios()
    funcionarios = [f for f in funcionarios if f.tipo != 'administrador']  # Exclui administradores
    projetos = db.listar_projetos()
    
    # Prepara dados para exibição
    registros_view = []
    total_horas = 0
    for registro in registros:
        funcionario = db.obter_usuario(registro.funcionario_id)
        projeto = db.obter_projeto(registro.projeto_id)
        
        registro_view = {
            'id': registro.id,
            'funcionario': funcionario.nome if funcionario else 'Desconhecido',
            'projeto': f"{projeto.id} | {projeto.nome}" if projeto else 'Desconhecido',
            'data': registro.data,
            'horas_trabalhadas': registro.horas_trabalhadas,
            # Passagens para o modal de edição
            'funcionario_id': registro.funcionario_id,
            'projeto_id': registro.projeto_id,
            'data_input': datetime.strptime(registro.data, "%m-%Y").strftime("%Y-%m"),
            'observacoes': registro.observacoes,
            # 'mes_ano_referencia': registro.mes_ano_referencia
        }
        registros_view.append(registro_view)
        total_horas += registro.horas_trabalhadas
        
    registros_view.sort(key=lambda x: x['id'], reverse=True)  # Ordena por ID decrescente inicialmente
    
    # Ordenação
    if ordenar:
        reverse = direcao == 'desc'
        if ordenar == 'colaborador':
            registros_view.sort(key=lambda x: x['funcionario'], reverse=reverse)
        elif ordenar == 'contrato':
            registros_view.sort(key=lambda x: x['projeto'], reverse=reverse)
        elif ordenar == 'data':
            registros_view.sort(key=lambda x: x['data'], reverse=not reverse)  # Mais recente primeiro

    # Pega os parâmetros atuais do link e remove o 'ordenar' e 'direcao' para montar uma nova ordem
    from urllib.parse import urlencode

    args_no_order = request.args.to_dict()
    args_no_order.pop('ordenar', None)
    args_no_order.pop('direcao', None)
    query_string = urlencode(args_no_order)

    # --- Paginação ---
    pagina = request.args.get('pagina', 1, type=int)
    # Pega quantos registros mostrar, padrão 5
    registros_por_pagina = request.args.get('registros_por_pagina', 5, type=int)
    total_registros = len(registros_view)
    inicio = (pagina - 1) * registros_por_pagina
    fim = inicio + registros_por_pagina
    registros_pag = registros_view[inicio:fim]
    total_paginas = (total_registros + registros_por_pagina - 1) // registros_por_pagina

    # query string atual sem página
    query_params = request.args.to_dict()
    if 'pagina' in query_params:
        del query_params['pagina']

    query_string_pages = '&'.join([f"{k}={v}" for k, v in query_params.items()])

    mostrando_inicio = (pagina - 1) * registros_por_pagina + 1
    mostrando_fim = min(pagina * registros_por_pagina, total_registros)
    total_resultados = total_registros


    return render_template(
        'registros/listar.html',
        usuario=usuario,
        registros=registros_pag,
        funcionarios=funcionarios,
        projetos=projetos,
        filtro_funcionario_id=funcionario_id,
        filtro_projeto_id=projeto_id,
        filtro_mes_ano=mes_ano,
        total_horas=total_horas,
        admin_check=admin_check,
        funcionario_logado=funcionario_id,
        mes_atual = datetime.now().strftime('%Y-%m'),
        query_string=query_string,
        ordenar=ordenar,
        direcao=direcao,
        query_string_pages=query_string_pages,
        total_paginas=total_paginas,
        pagina=pagina,
        registros_por_pagina=registros_por_pagina,
        mostrando_inicio=mostrando_inicio,
        mostrando_fim=mostrando_fim,
        total_resultados=total_resultados
    )

@registros_bp.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    """Adiciona um novo registro de horas."""
    # funcionarios = db.listar_funcionarios()
    # projetos = db.listar_projetos()

    usuario_id = session.get('usuario_id')
    usuario = db.obter_usuario(usuario_id)
    admin_check = usuario and usuario.tipo == 'administrador'

    if request.method == 'POST':

        # Se funcionário, força o próprio ID
        if admin_check:
            funcionario_id = request.form.get('funcionario_id', type=int)
        else:
            funcionario_id = usuario.id

        projeto_id = request.form.get('projeto_id', type=int)
        data_str = request.form.get('data')
        horas_trabalhadas = request.form.get('horas_trabalhadas', type=float)
        observacoes = request.form.get('observacoes').strip() or ''

        projetosEspeciais = [9010, 9014, 9021];

        if funcionario_id and projeto_id and data_str and horas_trabalhadas:
            try:
                data_obj = datetime.strptime(data_str, '%Y-%m')
                hoje = datetime.now()

                # Bloqueia se o mês for futuro
                if data_obj > hoje.replace(day=1):
                    flash('Não é possível adicionar registros para meses futuros.', 'danger')
                    return redirect(url_for('registros.listar'))

                # Se for o mês atual, limita pelas horas do dia atual
                if data_obj.month == hoje.month and data_obj.year == hoje.year:
                    limite_horas = hoje.day * 24  # Exemplo: dia 5 = 120 horas possíveis
                    if horas_trabalhadas > limite_horas:
                        flash(f'Não é possível adicionar mais de {limite_horas} horas no mês atual.', 'danger')
                        return redirect(url_for('registros.listar'))

                # Tudo certo, salva no formato MM-YYYY
                data = data_obj.strftime('%m-%Y')

                if projeto_id in projetosEspeciais:
                    if len(observacoes) < 5:
                        flash(f'É necessário inserir mais detalhes na observação desse GP.', 'danger')
                        return redirect(url_for('registros.listar'))

                registro = db.adicionar_registro_horas(
                    funcionario_id=funcionario_id,
                    projeto_id=projeto_id,
                    data=data,
                    horas_trabalhadas=horas_trabalhadas,
                    observacoes=observacoes
                )

                if registro:
                    flash('Registro de horas adicionado com sucesso!', 'success')
                    return redirect(url_for('registros.listar'))
                else:
                    flash('Erro ao adicionar registro de horas!', 'danger')
            except ValueError:
                flash('Formato de data inválido!', 'danger')
        else:
            flash('Todos os campos são obrigatórios!', 'danger')

    # mes_atual = datetime.now().strftime('%Y-%m')

    # return render_template(
    #     'registros/listar.html',
    #     funcionarios=funcionarios,
    #     projetos=projetos,
    #     admin_check=admin_check,
    #     funcionario_logado=usuario.funcionario_id if usuario and usuario.funcionario_id else None,
    #     mes_atual=mes_atual
    # )

@registros_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    """Edita um registro de horas existente."""
    registro = db.obter_registro_horas(id)
    if not registro:
        flash('Registro não encontrado!', 'danger')
        return redirect(url_for('registros.listar'))
    
    # funcionarios = db.listar_funcionarios()
    # projetos = db.listar_projetos()

    usuario_id = session.get('usuario_id')
    usuario = db.obter_usuario(usuario_id)
    admin_check = usuario and usuario.tipo == 'administrador'

    if request.method == 'POST':
        # Se funcionário, força o próprio ID
        if admin_check:
            funcionario_id = int(request.form.getlist('funcionario_id_edit')[0])  # Corrigido para obter o valor corretamente
        else:
            funcionario_id = usuario.id

        projeto_id = int(request.form.getlist('projeto_id_edit')[0])  # Corrigido para obter o valor corretamente
        data_str = request.form.get('data_edit')
        horas_trabalhadas = request.form.get('horas_edit', type=float)
        observacoes = request.form.get('observacoes_edit').strip() or ''

        projetosEspeciais = [9010, 9014, 9021];
        
        if funcionario_id and projeto_id and data_str and horas_trabalhadas:
            # Converte a data para o formato correto
            try:
                data_obj = datetime.strptime(data_str, '%Y-%m')
                hoje = datetime.now()

                # Bloqueia se o mês for futuro
                if data_obj > hoje.replace(day=1):
                    flash('Não é possível adicionar registros para meses futuros.', 'danger')
                    return redirect(url_for('registros.listar'))

                # Se for o mês atual, limita pelas horas do dia atual
                if data_obj.month == hoje.month and data_obj.year == hoje.year:
                    limite_horas = hoje.day * 24  # Exemplo: dia 5 = 120 horas possíveis
                    if horas_trabalhadas > limite_horas:
                        flash(f'Não é possível adicionar mais de {limite_horas} horas no mês atual.', 'danger')
                        return redirect(url_for('registros.listar'))

                # Tudo certo, salva no formato MM-YYYY
                data = data_obj.strftime('%m-%Y')

                if projeto_id in projetosEspeciais:
                    if len(observacoes) < 5:
                        flash(f'É necessário inserir mais detalhes na observação desse GP.', 'danger')
                        return redirect(url_for('registros.listar'))

                if db.atualizar_registro_horas(
                    id=id,
                    funcionario_id=funcionario_id,
                    projeto_id=projeto_id,
                    data=data,
                    horas_trabalhadas=horas_trabalhadas,
                    observacoes=observacoes
                ):
                    flash('Registro de horas atualizado com sucesso!', 'success')
                    return redirect(url_for('registros.listar'))
                else:
                    flash('Erro ao atualizar registro de horas!', 'danger')
            except ValueError:
                flash('Formato de data inválido!', 'danger')
        else:
            flash('Todos os campos são obrigatórios!', 'danger')

    # mes_atual = datetime.now().strftime('%Y-%m')
    
    # return render_template(
    #     'registros/listar.html',
    #     registro_selected=registro,
    #     # funcionarios=funcionarios,
    #     # projetos=projetos,
    #     # admin_check=admin_check,
    #     # funcionario_logado=usuario.funcionario_id if usuario and usuario.funcionario_id else None,
    #     data_input_value=data_input_value,
    #     # mes_atual=mes_atual
    # )

@registros_bp.route('/remover/<int:id>', methods=['POST'])
def remover(id):
    """Remove um registro de horas."""
    if db.remover_registro_horas(id):
        flash('Registro de horas removido com sucesso!', 'success')
    else:
        flash('Erro ao remover registro de horas!', 'danger')
    
    return redirect(url_for('registros.listar'))

@registros_bp.route('/exportar', methods=['GET'])
def exportar():
    """Exibe a página de exportação de relatórios."""
    funcionarios = db.listar_usuarios()
    # Remover admin da lista
    funcionarios = [f for f in funcionarios if f.tipo != 'administrador']
    
    projetos = db.listar_projetos()

    # Obtém o usuário atual
    usuario_id = session.get('usuario_id')
    usuario = db.obter_usuario(usuario_id)
    admin_check = usuario and usuario.tipo == 'administrador'

    # Se funcionário, força o próprio ID
    if admin_check:
        funcionario_id = request.args.get('funcionario_id_filter', type=int)
    else:
        funcionario_id = usuario.id
    
    # Obtém a lista de meses/anos disponíveis
    meses_anos = set()
    for registro in db.registros_horas:
        if registro.data:
            meses_anos.add(registro.data)
    
    meses_anos = sorted(list(meses_anos))
    
    return render_template(
        'registros/exportar.html',
        admin_check=admin_check,
        funcionario_logado=funcionario_id,
        usuario=usuario,
        funcionarios=funcionarios,
        projetos=projetos,
        meses_anos=meses_anos
    )

@registros_bp.route('/exportar/excel', methods=['POST'])
def exportar_excel():
    """Exporta os registros filtrados para um arquivo Excel."""
    funcionario_id = request.form.get('funcionario_id', type=int)
    projeto_id = request.form.get('projeto_id', type=int)
    mes_ano = request.form.get('mes_ano')
    tipo_relatorio = request.form.get('tipo_relatorio', 'padrao')
    
    # Obtém os registros filtrados
    registros = db.listar_registros_horas(
        funcionario_id=funcionario_id,
        projeto_id=projeto_id,
        mes_ano=mes_ano
    )
    
    # Prepara dados para o DataFrame
    dados = []
    for registro in registros:
        funcionario = db.obter_usuario(registro.funcionario_id)
        projeto = db.obter_projeto(registro.projeto_id)
        
        dados.append({
            'ID': registro.id,
            'Funcionário': funcionario.nome if funcionario else 'Desconhecido',
            'Projeto': projeto.nome if projeto else 'Desconhecido',
            # 'Data': registro.data,
            'Horas': registro.horas_trabalhadas,
            'Mês/Ano': registro.data,
            'ID_Funcionario': registro.funcionario_id,
            'ID_Projeto': registro.projeto_id
        })
    
    if not dados:
        flash('Nenhum registro encontrado para exportação!', 'warning')
        return redirect(url_for('registros.exportar'))
    
    # Cria o DataFrame
    df = pd.DataFrame(dados)
    
    # Nome do arquivo temporário para o Excel
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
    temp_file.close()
    
    # Gera o relatório de acordo com o tipo selecionado
    if tipo_relatorio == 'padrao':
        _gerar_relatorio_padrao(df, temp_file.name)
    elif tipo_relatorio == 'por_funcionario':
        _gerar_relatorio_por_funcionario(df, temp_file.name)
    elif tipo_relatorio == 'por_projeto':
        _gerar_relatorio_por_projeto(df, temp_file.name)
    elif tipo_relatorio == 'mensal':
        _gerar_relatorio_mensal(df, temp_file.name)
    else:
        _gerar_relatorio_padrao(df, temp_file.name)
    
    # Define o nome do arquivo para download
    nome_arquivo = f'controle_horas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    # Envia o arquivo para download
    return send_file(
        temp_file.name,
        as_attachment=True,
        download_name=nome_arquivo,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@registros_bp.route('/exportar/personalizado', methods=['POST'])
@login_required
def exportar_personalizado():
    """Exporta os registros para Excel no formato personalizado do template."""
    funcionario_id = request.form.get('funcionario_id', type=int)
    projeto_id = request.form.get('projeto_id', type=int)
    mes_ano = request.form.get('mes_ano')
    
    # # Verificar se o usuário é administrador ou funcionário
    # usuario_id = session.get('usuario_id')
    # usuario = db.obter_usuario(usuario_id)
    
    # # Se for funcionário, força o filtro pelo seu próprio ID
    # if usuario and usuario.tipo == 'funcionario' and usuario.funcionario_id:
    #     funcionario_id = usuario.funcionario_id
    
    # Usar o formato personalizado do template
    try:
        arquivo_excel = adaptar_exportacao_relatorio_mensal(
            db=db,
            funcionario_id=funcionario_id,
            projeto_id=projeto_id,
            mes_ano=mes_ano
        )
        
        # Enviar o arquivo
        return send_file(
            arquivo_excel,
            as_attachment=True,
            download_name=f"controle_horas_template_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        flash(f'Erro ao gerar relatório personalizado: {str(e)}', 'danger')
        return redirect(url_for('registros.exportar'))

def _gerar_relatorio_padrao(df, arquivo):
    """Gera um relatório padrão com todos os registros."""
    # Remove colunas de IDs internos
    df_export = (
        df.drop(columns=['ID', 'ID_Funcionario', 'ID_Projeto'])
        .sort_values(by='Mês/Ano', key=lambda col: pd.to_datetime(col, format='%m-%Y'))
    )
    
    # Cria um escritor Excel
    writer = pd.ExcelWriter(arquivo, engine='xlsxwriter')
    
    # Escreve os dados na planilha
    df_export.to_excel(writer, sheet_name='Registros', index=False)
    
    # Obtém o objeto de planilha
    workbook = writer.book
    worksheet = writer.sheets['Registros']
    
    # Adiciona uma linha de total
    total_row = len(df_export) + 1
    worksheet.write(total_row, 0, 'Total')
    worksheet.write_formula(total_row, 2, f'=SUM(C2:C{total_row})')
    
    # Formata a coluna de horas
    format_horas = workbook.add_format({'num_format': '0.00'})
    
    # Aplica tamanho padrao nas colunas
    aplicar_padrao_colunas(worksheet)
    
    # Salva o arquivo
    writer.close()

def _gerar_relatorio_por_funcionario(df, arquivo):
    """Gera um relatório agrupado por funcionário."""
    # Cria um escritor Excel
    writer = pd.ExcelWriter(arquivo, engine='xlsxwriter')
    
    # Agrupa por funcionário
    for funcionario, grupo in df.groupby('Funcionário'):
        # Remove colunas desnecessárias
        df_export = (
        grupo.drop(columns=['ID', 'ID_Funcionario', 'ID_Projeto'])
        .sort_values(by='Mês/Ano', key=lambda col: pd.to_datetime(col, format='%m-%Y'))
    )
        
        # Escreve os dados na planilha
        sheet_name = funcionario[:31]  # Limita o nome da planilha a 31 caracteres
        df_export.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Obtém o objeto de planilha
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        
        # Adiciona uma linha de total
        total_row = len(df_export) + 1
        worksheet.write(total_row, 0, 'Total')
        worksheet.write_formula(total_row, 2, f'=SUM(C2:C{total_row})')
        
        # Formata a coluna de horas
        format_horas = workbook.add_format({'num_format': '0.00'})
        
        # Aplica tamanho padrao nas colunas
        aplicar_padrao_colunas(worksheet)
    
    # Adiciona uma planilha de resumo
    resumo = df.groupby('Funcionário')['Horas'].sum().reset_index()
    resumo.to_excel(writer, sheet_name='Resumo', index=False)
    
    worksheet = writer.sheets['Resumo']
    aplicar_padrao_colunas(worksheet)
    total_row = len(resumo) + 1
    worksheet.write(total_row, 0, 'Total Geral')
    worksheet.write_formula(total_row, 1, f'=SUM(B2:B{total_row})')
    
    # Salva o arquivo
    writer.close()

def _gerar_relatorio_por_projeto(df, arquivo):
    """Gera um relatório agrupado por projeto."""
    # Cria um escritor Excel
    writer = pd.ExcelWriter(arquivo, engine='xlsxwriter')
    
    # Agrupa por projeto
    for projeto, grupo in df.groupby('Projeto'):
        # Remove colunas desnecessárias
        df_export = grupo.drop(columns=['ID', 'ID_Funcionario', 'ID_Projeto'])
        
        # Escreve os dados na planilha
        sheet_name = projeto[:31]  # Limita o nome da planilha a 31 caracteres
        df_export.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Obtém o objeto de planilha
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        
        # Adiciona uma linha de total
        total_row = len(df_export) + 1
        worksheet.write(total_row, 0, 'Total')
        worksheet.write_formula(total_row, 2, f'=SUM(C2:C{total_row})')
        
        # Formata a coluna de horas
        format_horas = workbook.add_format({'num_format': '0.00'})
        
        # Aplica tamanho padrao nas colunas
        aplicar_padrao_colunas(worksheet)
    
    # Adiciona uma planilha de resumo
    resumo = df.groupby('Projeto')['Horas'].sum().reset_index()
    resumo.to_excel(writer, sheet_name='Resumo', index=False)
    
    worksheet = writer.sheets['Resumo']
    aplicar_padrao_colunas(worksheet)
    total_row = len(resumo) + 1
    worksheet.write(total_row, 0, 'Total Geral')
    worksheet.write_formula(total_row, 1, f'=SUM(B2:B{total_row})')
    
    # Salva o arquivo
    writer.close()

def _gerar_relatorio_mensal(df, arquivo):
    """Gera um relatório mensal com matriz de funcionários x projetos."""
    # Cria um escritor Excel
    writer = pd.ExcelWriter(arquivo, engine='xlsxwriter')
    
    # Agrupa por mês/ano
    for mes_ano, grupo in df.groupby('Mês/Ano'):
        # Cria uma tabela dinâmica: Funcionários nas linhas, Projetos nas colunas
        pivot = pd.pivot_table(
            grupo,
            values='Horas',
            index=['Funcionário'],
            columns=['Projeto'],
            aggfunc='sum',
            fill_value=0
        )
        
        # Adiciona uma coluna de total por funcionário
        pivot['Total'] = pivot.sum(axis=1)
        
        # Adiciona uma linha de total por projeto
        totais = pivot.sum().to_frame().T
        totais.index = ['Total']
        pivot_final = pd.concat([pivot, totais])
        
        # Escreve os dados na planilha
        sheet_name = mes_ano if mes_ano else 'Sem Data'
        pivot_final.to_excel(writer, sheet_name=sheet_name)
        
        # Obtém o objeto de planilha
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        
        # Formata os números
        format_horas = workbook.add_format({'num_format': '0.00'})
        
        # Aplica formato a todas as células de dados
        for col in range(1, len(pivot_final.columns) + 1):
            for row in range(1, len(pivot_final) + 1):
                worksheet.write(row, col, pivot_final.iloc[row-1, col-1], format_horas)
        
        # Destaca a coluna e linha de totais
        format_total = workbook.add_format({
            'bold': True,
            'num_format': '0.00',
            'bg_color': '#E0E0E0'
        })
        
        # Aplica formato à coluna de total
        for row in range(1, len(pivot_final)):
            worksheet.write(row, len(pivot_final.columns), pivot_final.iloc[row-1, -1], format_total)
        
        # Aplica formato à linha de total
        for col in range(1, len(pivot_final.columns) + 1):
            worksheet.write(len(pivot_final), col, pivot_final.iloc[-1, col-1], format_total)
        
        # Ajusta a largura das colunas
        worksheet.set_column(0, 0, 20)  # Coluna de funcionários
        for col in range(1, len(pivot_final.columns) + 1):
            worksheet.set_column(col, col, 20)
    
    # Salva o arquivo
    writer.close()

# Padrão de tamanho de cada coluna nas planilhas
PADRAO_COLUNAS = {
    'A:A': 30,  # Funcionário
    'B:B': 30,  # Projeto
    'C:C': 10,  # Mês/Ano
    'D:D': 10   # Horas
}

# Aplica os tamanhos padrões
def aplicar_padrao_colunas(worksheet):
    for coluna, largura in PADRAO_COLUNAS.items():
        worksheet.set_column(coluna, largura)
