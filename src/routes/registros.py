from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, send_file, session
from src.models.database import db
from src.utils.auth_utils import login_required, admin_required
from src.utils.relatorio_personalizado import adaptar_exportacao_relatorio_mensal
from datetime import datetime
import pandas as pd
import os
import tempfile

registros_bp = Blueprint('registros', __name__)

@registros_bp.route('/')
@login_required
def listar():
    """Exibe a lista de registros de horas com base nas permissões do usuário."""
    # Parâmetros de filtro opcionais
    funcionario_id = request.args.get('funcionario_id', type=int)
    projeto_id = request.args.get('projeto_id', type=int)
    mes_ano = request.args.get('mes_ano')
    ordenar = request.args.get('ordenar', 'data')
    
    # Obtém o usuário atual
    usuario_id = session.get('usuario_id')
    usuario = db.obter_usuario(usuario_id)
    
    # Se for funcionário, força o filtro pelo seu próprio ID
    if usuario and usuario.tipo == 'funcionario' and usuario.funcionario_id:
        funcionario_id = usuario.funcionario_id
    
    # Obtém os registros filtrados
    registros = db.listar_registros_horas(
        funcionario_id=funcionario_id,
        projeto_id=projeto_id,
        mes_ano=mes_ano
    )
    
    # Obtém listas de funcionários e projetos para os filtros
    funcionarios = db.listar_funcionarios()
    projetos = db.listar_projetos()
    
    # Prepara dados para exibição
    registros_view = []
    total_horas = 0
    for registro in registros:
        funcionario = db.obter_funcionario(registro.funcionario_id)
        projeto = db.obter_projeto(registro.projeto_id)
        
        registro_view = {
            'id': registro.id,
            'funcionario': funcionario.nome if funcionario else 'Desconhecido',
            'projeto': f"{projeto.id} | {projeto.nome}" if projeto else 'Desconhecido',
            'data': registro.data,
            'horas_trabalhadas': registro.horas_trabalhadas,
            'mes_ano_referencia': registro.mes_ano_referencia
        }
        registros_view.append(registro_view)
        total_horas += registro.horas_trabalhadas
    
    # Ordenação
    if ordenar == 'colaborador':
        registros_view.sort(key=lambda x: x['funcionario'])
    elif ordenar == 'contrato':
        registros_view.sort(key=lambda x: x['projeto'])
    elif ordenar == 'data':
        registros_view.sort(key=lambda x: x['data'], reverse=True)  # Mais recente primeiro
    
    # Prepara dados agregados por mês/ano
    registros_agregados = {}
    for registro_view in registros_view:
        chave = (registro_view['funcionario'], registro_view['projeto'], registro_view['mes_ano_referencia'])
        if chave not in registros_agregados:
            registros_agregados[chave] = {
                'colaborador': registro_view['funcionario'],
                'contrato': registro_view['projeto'],
                'mes_ano': registro_view['mes_ano_referencia'],
                'total_horas': 0
            }
        registros_agregados[chave]['total_horas'] += registro_view['horas_trabalhadas']
    
    # Converte para lista e ordena por mês/ano
    registros_agregados_list = list(registros_agregados.values())
    registros_agregados_list.sort(key=lambda x: (x['mes_ano'], x['colaborador'], x['contrato']), reverse=True)
    
    return render_template(
        'registros/listar.html',
        registros=registros_view,
        registros_agregados=registros_agregados_list,
        funcionarios=funcionarios,
        projetos=projetos,
        filtro_funcionario_id=funcionario_id,
        filtro_projeto_id=projeto_id,
        filtro_mes_ano=mes_ano,
        total_horas=total_horas,
        total_horas_agregado=total_horas
    )

@registros_bp.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    """Adiciona um novo registro de horas."""
    funcionarios = db.listar_funcionarios()
    projetos = db.listar_projetos()
    
    if request.method == 'POST':
        funcionario_id = request.form.get('funcionario_id', type=int)
        projeto_id = request.form.get('projeto_id', type=int)
        data_str = request.form.get('data')
        horas_trabalhadas = request.form.get('horas_trabalhadas', type=float)
        
        if funcionario_id and projeto_id and data_str and horas_trabalhadas:
            # Converte a data para o formato correto
            try:
                data = datetime.strptime(data_str, '%Y-%m-%d').strftime('%Y-%m-%d')
                registro = db.adicionar_registro_horas(
                    funcionario_id=funcionario_id,
                    projeto_id=projeto_id,
                    data=data,
                    horas_trabalhadas=horas_trabalhadas
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
    
    return render_template('registros/adicionar.html', funcionarios=funcionarios, projetos=projetos)

@registros_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    """Edita um registro de horas existente."""
    registro = db.obter_registro_horas(id)
    if not registro:
        flash('Registro não encontrado!', 'danger')
        return redirect(url_for('registros.listar'))
    
    funcionarios = db.listar_funcionarios()
    projetos = db.listar_projetos()
    
    if request.method == 'POST':
        funcionario_id = request.form.get('funcionario_id', type=int)
        projeto_id = request.form.get('projeto_id', type=int)
        data_str = request.form.get('data')
        horas_trabalhadas = request.form.get('horas_trabalhadas', type=float)
        
        if funcionario_id and projeto_id and data_str and horas_trabalhadas:
            # Converte a data para o formato correto
            try:
                data = datetime.strptime(data_str, '%Y-%m-%d').strftime('%Y-%m-%d')
                if db.atualizar_registro_horas(
                    id=id,
                    funcionario_id=funcionario_id,
                    projeto_id=projeto_id,
                    data=data,
                    horas_trabalhadas=horas_trabalhadas
                ):
                    flash('Registro de horas atualizado com sucesso!', 'success')
                    return redirect(url_for('registros.listar'))
                else:
                    flash('Erro ao atualizar registro de horas!', 'danger')
            except ValueError:
                flash('Formato de data inválido!', 'danger')
        else:
            flash('Todos os campos são obrigatórios!', 'danger')
    
    return render_template(
        'registros/editar.html',
        registro=registro,
        funcionarios=funcionarios,
        projetos=projetos
    )

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
    funcionarios = db.listar_funcionarios()
    projetos = db.listar_projetos()
    
    # Obtém a lista de meses/anos disponíveis
    meses_anos = set()
    for registro in db.registros_horas:
        if registro.mes_ano_referencia:
            meses_anos.add(registro.mes_ano_referencia)
    
    meses_anos = sorted(list(meses_anos))
    
    return render_template(
        'registros/exportar.html',
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
        funcionario = db.obter_funcionario(registro.funcionario_id)
        projeto = db.obter_projeto(registro.projeto_id)
        
        dados.append({
            'ID': registro.id,
            'Funcionário': funcionario.nome if funcionario else 'Desconhecido',
            'Projeto': projeto.nome if projeto else 'Desconhecido',
            'Data': registro.data,
            'Horas': registro.horas_trabalhadas,
            'Mês/Ano': registro.mes_ano_referencia,
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
    
    # Verificar se o usuário é administrador ou funcionário
    usuario_id = session.get('usuario_id')
    usuario = db.obter_usuario(usuario_id)
    
    # Se for funcionário, força o filtro pelo seu próprio ID
    if usuario and usuario.tipo == 'funcionario' and usuario.funcionario_id:
        funcionario_id = usuario.funcionario_id
    
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
    df_export = df.drop(columns=['ID', 'ID_Funcionario', 'ID_Projeto'])
    
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
    worksheet.write_formula(total_row, 3, f'=SUM(D2:D{total_row})')
    
    # Formata a coluna de horas
    format_horas = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('D:D', 10, format_horas)
    
    # Formata a coluna de data
    format_data = workbook.add_format({'num_format': 'yyyy-mm-dd'})
    worksheet.set_column('C:C', 12, format_data)
    
    # Ajusta a largura das colunas
    worksheet.set_column('A:A', 20)  # Funcionário
    worksheet.set_column('B:B', 30)  # Projeto
    worksheet.set_column('E:E', 10)  # Mês/Ano
    
    # Salva o arquivo
    writer.close()

def _gerar_relatorio_por_funcionario(df, arquivo):
    """Gera um relatório agrupado por funcionário."""
    # Cria um escritor Excel
    writer = pd.ExcelWriter(arquivo, engine='xlsxwriter')
    
    # Agrupa por funcionário
    for funcionario, grupo in df.groupby('Funcionário'):
        # Remove colunas desnecessárias
        df_export = grupo.drop(columns=['ID', 'ID_Funcionario', 'ID_Projeto'])
        
        # Escreve os dados na planilha
        sheet_name = funcionario[:31]  # Limita o nome da planilha a 31 caracteres
        df_export.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Obtém o objeto de planilha
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        
        # Adiciona uma linha de total
        total_row = len(df_export) + 1
        worksheet.write(total_row, 0, 'Total')
        worksheet.write_formula(total_row, 3, f'=SUM(D2:D{total_row})')
        
        # Formata a coluna de horas
        format_horas = workbook.add_format({'num_format': '0.00'})
        worksheet.set_column('D:D', 10, format_horas)
        
        # Formata a coluna de data
        format_data = workbook.add_format({'num_format': 'yyyy-mm-dd'})
        worksheet.set_column('C:C', 12, format_data)
        
        # Ajusta a largura das colunas
        worksheet.set_column('A:A', 20)  # Funcionário
        worksheet.set_column('B:B', 30)  # Projeto
        worksheet.set_column('E:E', 10)  # Mês/Ano
    
    # Adiciona uma planilha de resumo
    resumo = df.groupby('Funcionário')['Horas'].sum().reset_index()
    resumo.to_excel(writer, sheet_name='Resumo', index=False)
    
    worksheet = writer.sheets['Resumo']
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
        worksheet.write_formula(total_row, 3, f'=SUM(D2:D{total_row})')
        
        # Formata a coluna de horas
        format_horas = workbook.add_format({'num_format': '0.00'})
        worksheet.set_column('D:D', 10, format_horas)
        
        # Formata a coluna de data
        format_data = workbook.add_format({'num_format': 'yyyy-mm-dd'})
        worksheet.set_column('C:C', 12, format_data)
        
        # Ajusta a largura das colunas
        worksheet.set_column('A:A', 20)  # Funcionário
        worksheet.set_column('B:B', 30)  # Projeto
        worksheet.set_column('E:E', 10)  # Mês/Ano
    
    # Adiciona uma planilha de resumo
    resumo = df.groupby('Projeto')['Horas'].sum().reset_index()
    resumo.to_excel(writer, sheet_name='Resumo', index=False)
    
    worksheet = writer.sheets['Resumo']
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
            worksheet.set_column(col, col, 12)
    
    # Salva o arquivo
    writer.close()
