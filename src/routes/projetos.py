from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, session
from src.models.database import db
from src.utils.auth_utils import login_required, admin_required
import logging
from markupsafe import Markup

projetos_bp = Blueprint('contratos', __name__)

@projetos_bp.route('/', methods=['GET'])
@login_required
def listar():
    """Exibe a lista de projetos."""

    # Obtém o usuário atual
    usuario_id = session.get('usuario_id')
    usuario = db.obter_usuario(usuario_id)
    admin_check = usuario and usuario.tipo == 'administrador'

    projetos = db.listar_projetos()
    total_projetos = len(projetos)

    # Parâmetros de filtro opcionais
    ordenar = request.args.get('ordenar', 'nome')
    direcao = request.args.get('direcao', 'asc')

    # Ordenação
    if ordenar:
        reverse = direcao == 'desc'
        if ordenar == 'cod':
            projetos.sort(key=lambda p: p.id, reverse=reverse)
        elif ordenar == 'nome':
            projetos.sort(key=lambda p: p.nome, reverse=reverse)

    # Pega os parâmetros atuais do link e remove o 'ordenar' e 'direcao' para montar uma nova ordem
    from urllib.parse import urlencode

    args_no_order = request.args.to_dict()
    args_no_order.pop('ordenar', None)
    args_no_order.pop('direcao', None)
    query_string = urlencode(args_no_order)

    # --- Parâmetro de busca ---
    search = request.args.get('search', '').strip().lower()

    # --- Caso tenha busca, filtra ---
    if search:
        projetos = [
            p for p in projetos
            if search in p.nome.lower()
            or search in str(p.id).lower()
        ]
    
    # --- Paginação ---
    pagina = request.args.get('pagina', 1, type=int)
    # Pega quantos contratos mostrar, padrão 5
    contratos_por_pagina = request.args.get('contratos_por_pagina', 5, type=int)
    total_contratos = len(projetos)
    inicio = (pagina - 1) * contratos_por_pagina
    fim = inicio + contratos_por_pagina
    contratos_pag = projetos[inicio:fim]
    total_paginas = (total_contratos + contratos_por_pagina - 1) // contratos_por_pagina

    # query string atual sem página
    query_params = request.args.to_dict()
    if 'pagina' in query_params:
        del query_params['pagina']

    query_string_pages = '&'.join([f"{k}={v}" for k, v in query_params.items()])

    mostrando_inicio = (pagina - 1) * contratos_por_pagina + 1
    mostrando_fim = min(pagina * contratos_por_pagina, total_contratos)
    total_resultados = total_contratos

    return render_template(
        'projetos/listar.html',
        db=db,
        usuario=usuario,
        projetos=contratos_pag,
        admin_check=admin_check,
        total_projetos=total_projetos,
        search=search if search else None,
        query_string=query_string,
        ordenar=ordenar,
        direcao=direcao,
        query_string_pages=query_string_pages,
        total_paginas=total_paginas,
        pagina=pagina,
        contratos_por_pagina=contratos_por_pagina,
        mostrando_inicio=mostrando_inicio,
        mostrando_fim=mostrando_fim,
        total_resultados=total_resultados
    )

@projetos_bp.route('/detalhes/<int:id>')
@admin_required
def detalhes(id):
    """Exibe os detalhes de um projeto. Acesso restrito a administradores."""

    # Obtém o usuário atual
    usuario_id = session.get('usuario_id')
    usuario = db.obter_usuario(usuario_id)
    admin_check = usuario and usuario.tipo == 'administrador'

    projeto = db.obter_projeto(id)
    if not projeto:
        flash('Projeto não encontrado!', 'danger')
        return redirect(url_for('contratos.listar'))
    
    return render_template(
        'projetos/detalhes.html',
        usuario=usuario,
        admin_check=admin_check,
        projeto=projeto,
        db=db)

@projetos_bp.route('/remover/<int:id>', methods=['POST'])
@admin_required
def remover(id):
    """Remove um projeto. Acesso restrito a administradores."""
    
    projeto = db.obter_projeto(id)

    try:
        sucesso = db.remover_projeto(id)
        if sucesso:
            flash(
                Markup(f"Contrato <strong>{projeto.id} - {projeto.nome}</strong> removido com sucesso!"), 'success'
            )
            logging.info(f"Contrato ID={id} removido do sistema.")
        else:
            flash('Erro ao remover contrato. Verifique se ele está cadastrado.', 'danger')
    except Exception as e:
        logging.exception("Erro ao remover contrato:")
        flash(f"Erro inesperado ao remover contrato {projeto.id} - {projeto.nome}.", 'danger')

    return redirect(url_for('contratos.listar'))

# API para uso em AJAX
@projetos_bp.route('/api/listar', methods=['GET'])
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
            return redirect(url_for('contratos.listar'))
        
        arquivo = request.files['arquivo_contratos']
        if arquivo.filename == '':
            flash('Nenhum arquivo foi selecionado!', 'danger')
            return redirect(url_for('contratos.listar'))
        
        if not arquivo.filename.lower().endswith(('.xlsx', '.xls')):
            flash('Formato de arquivo inválido! Use apenas arquivos Excel (.xlsx ou .xls)', 'danger')
            return redirect(url_for('contratos.listar'))
        
        # Lê o arquivo Excel
        df = pd.read_excel(arquivo)
        
        # Verifica se o arquivo tem pelo menos 2 colunas
        if len(df.columns) < 2:
            flash('O arquivo deve ter pelo menos 2 colunas (ID e Nome)!', 'danger')
            return redirect(url_for('contratos.listar'))
        
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
                projeto_existente = db.obter_projeto(contrato_id)
                
                if projeto_existente:
                    # Atualiza o nome se for diferente
                    if projeto_existente.nome != contrato_nome:
                        db.atualizar_projeto(projeto_existente.id, contrato_nome)
                        contratos_atualizados += 1
                else:
                    # Adiciona novo contrato
                    db.adicionar_projeto(contrato_id, contrato_nome)
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
            flash('Nenhum contrato foi importado. Verifique o formato do arquivo ou se o contrato já foi cadastrado.', 'warning')
            
    except Exception as e:
        flash(f'Erro ao processar arquivo: {str(e)}', 'danger')
    
    return redirect(url_for('contratos.listar'))

