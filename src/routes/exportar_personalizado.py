from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, send_file, session
from src.models.database import db
from src.utils.auth_utils import login_required, admin_required
from src.utils.relatorio_personalizado import adaptar_exportacao_relatorio_mensal
from datetime import datetime
import os

# Importar o blueprint de registros
from src.routes.registros import registros_bp

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
