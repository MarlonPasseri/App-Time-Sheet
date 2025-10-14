from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session
from src.models.database import db
from src.utils.auth_utils import login_required, admin_required

projetos_bp = Blueprint('projetos', __name__)

@projetos_bp.route('/')
@login_required
def listar():
    """Exibe a lista de projetos."""
    projetos = db.listar_projetos()
    return render_template('projetos/listar.html', projetos=projetos)

@projetos_bp.route('/detalhes/<int:id>')
@admin_required
def detalhes(id):
    """Exibe os detalhes de um projeto. Acesso restrito a administradores."""
    projeto = db.obter_projeto(id)
    if not projeto:
        flash('Projeto não encontrado!', 'danger')
        return redirect(url_for('projetos.listar'))
    
    return render_template('projetos/detalhes.html', projeto=projeto, db=db)

# API para uso em AJAX
@projetos_bp.route('/api/listar', methods=['GET'])
@login_required
def api_listar():
    """Retorna a lista de projetos em formato JSON."""
    projetos = db.listar_projetos()
    return jsonify([p.to_dict() for p in projetos])

@projetos_bp.route('/importar_lista', methods=['POST'])
@admin_required
def importar_lista():
    """Importa uma lista de contratos a partir de um arquivo Excel."""
    import pandas as pd
    from werkzeug.utils import secure_filename
    import os
    
    try:
        if 'arquivo_contratos' not in request.files:
            flash('Nenhum arquivo foi selecionado!', 'danger')
            return redirect(url_for('projetos.listar'))
        
        arquivo = request.files['arquivo_contratos']
        if arquivo.filename == '':
            flash('Nenhum arquivo foi selecionado!', 'danger')
            return redirect(url_for('projetos.listar'))
        
        if not arquivo.filename.lower().endswith(('.xlsx', '.xls')):
            flash('Formato de arquivo inválido! Use apenas arquivos Excel (.xlsx ou .xls)', 'danger')
            return redirect(url_for('projetos.listar'))
        
        # Lê o arquivo Excel
        df = pd.read_excel(arquivo)
        
        # Verifica se o arquivo tem pelo menos 2 colunas
        if len(df.columns) < 2:
            flash('O arquivo deve ter pelo menos 2 colunas (ID e Nome)!', 'danger')
            return redirect(url_for('projetos.listar'))
        
        # Assume que as duas primeiras colunas são ID e Nome
        df.columns = ['id', 'nome'] + list(df.columns[2:])
        
        contratos_importados = 0
        contratos_atualizados = 0
        
        for index, row in df.iterrows():
            try:
                # Converte o ID para string para permitir IDs como "GP9014"
                contrato_id = str(row['id']).strip()
                contrato_nome = str(row['nome']).strip()
                
                # Pula linhas vazias ou com dados inválidos
                if pd.isna(row['id']) or pd.isna(row['nome']) or contrato_nome == '':
                    continue
                
                # Verifica se o contrato já existe
                projeto_existente = db.obter_projeto_por_id_string(contrato_id)
                
                if projeto_existente:
                    # Atualiza o nome se for diferente
                    if projeto_existente.nome != contrato_nome:
                        db.atualizar_projeto(projeto_existente.id, contrato_nome)
                        contratos_atualizados += 1
                else:
                    # Adiciona novo contrato
                    db.adicionar_projeto_com_id_customizado(contrato_id, contrato_nome)
                    contratos_importados += 1
                    
            except Exception as e:
                flash(f'Erro ao processar linha {index + 1}: {str(e)}', 'warning')
                continue
        
        if contratos_importados > 0 or contratos_atualizados > 0:
            mensagem = f'Importação concluída! {contratos_importados} contratos importados'
            if contratos_atualizados > 0:
                mensagem += f', {contratos_atualizados} contratos atualizados'
            flash(mensagem, 'success')
        else:
            flash('Nenhum contrato foi importado. Verifique o formato do arquivo.', 'warning')
            
    except Exception as e:
        flash(f'Erro ao processar arquivo: {str(e)}', 'danger')
    
    return redirect(url_for('projetos.listar'))
