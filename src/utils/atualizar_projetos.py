import json
import os

def atualizar_projetos():
    # Lista de projetos do arquivo enviado pelo usuário
    novos_projetos = [
        {"id": "656", "nome": "Nexa - Barragem do Peixe"},
        {"id": "669", "nome": "Nexa - Barragem das Pedras"},
        {"id": "1796", "nome": "Senac - Instrumentação"},
        {"id": "1881", "nome": "Enel - Serviços de Consultoria por demandas"},
        {"id": "1905", "nome": "Ecovix - Instrumentação"},
        {"id": "1924", "nome": "MRS - Instrumentação Barbacena"},
        {"id": "2139", "nome": "Heb - Prédio em Campos"},
        {"id": "2240", "nome": "Enel - Frame Civil"},
        {"id": "2298", "nome": "Hydro - Instrumentação"},
        {"id": "2317", "nome": "Comosa - PCH Mosquitão"},
        {"id": "2339", "nome": "Vale - Manutenção"},
        {"id": "2359", "nome": "Braskem - Instrumentação Maceió"},
        {"id": "2396", "nome": "Pavidez - Hydro Fase 3"},
        {"id": "2400", "nome": "Seel - Coronel Domiciano"},
        {"id": "2449", "nome": "Alumar - Instrumentação ARB 8 e 9"},
        {"id": "2510", "nome": "Vale - Consultoria Instrumentação"},
        {"id": "2516", "nome": "Braskem - Apoio Comite"},
        {"id": "2548", "nome": "CCR - BR-101 e BR-116"},
        {"id": "2556", "nome": "NTS - Instrumentação"},
        {"id": "2565", "nome": "Hydro - Automação"},
        {"id": "2585", "nome": "Kinfra - KM-217=850 da BR-393RJ"},
        {"id": "2586", "nome": "Enel - Laranja Doce"},
        {"id": "2597", "nome": "Puc - Perreira Passos"},
        {"id": "2602", "nome": "SEFAC - Serra do Fação"},
        {"id": "2623", "nome": "Vale - Mina do Caue - Itabira"},
        {"id": "2664", "nome": "Pavidez - Reabilitação DRS 1 - Fase 04"},
        {"id": "2667", "nome": "EDF - Taludes Serra do Seridó"},
        {"id": "2678", "nome": "Sefac - Erosões 6 e 73"},
        {"id": "2704", "nome": "Possebon - Projeto Executivo"},
        {"id": "2712", "nome": "Vale - Contrato ACG - Instrumentação Convencional"},
        {"id": "2718", "nome": "Alumar - Investigações Geotécnicas"},
        {"id": "2747", "nome": "Hydro - Instalação e Automação"},
        {"id": "2775", "nome": "Ecorodovia - Investigação Geológica"},
        {"id": "2786", "nome": "EDF - Serra de Seridó Fase II"},
        {"id": "2857", "nome": "Braskem - Inc - São Miguel dos Campos"},
        {"id": "2868", "nome": "Const. União Realizações - Instrumentação"},
        {"id": "2880", "nome": "Alumar - Instrumentação ARB10"},
        {"id": "2888", "nome": "CIMCOP - Projeto Brucutu"},
        {"id": "2913", "nome": "Light - Segurança de Barragem"},
        {"id": "2915", "nome": "Furnas - Campo do Meio"},
        {"id": "2917", "nome": "PXENERGY - São Mateus do Sul"},
        {"id": "2919", "nome": "Sesc - Pantanal"},
        {"id": "2920", "nome": "Ecorodovia - Rio-Minas - Manilha-Magé"},
        {"id": "2934", "nome": "UFES - Estudo Geotécnico"},
        {"id": "2942", "nome": "Alumar - Lagoa de Água Bruta"},
        {"id": "2943", "nome": "MAFRIGEO - Barragens Sertãozinho (SP)"},
        {"id": "2946", "nome": "Copasa - Monte Carlos"},
        {"id": "2950", "nome": "NOVA 381 - Concessão BR-381"},
        {"id": "2952", "nome": "PXENERGY - RISP - São Mateus do Sul"},
        {"id": "2969", "nome": "Alumar - Sondagem do DET 1"},
        {"id": "2978", "nome": "EPR - Instrumentação"},
        {"id": "2982", "nome": "Vale Verde - PDE Cavalo - Fase 1"},
        {"id": "2983", "nome": "EGIS - Geotecnica e Contenção - BR-101"},
        {"id": "2985", "nome": "EPR - Levantamento de Campo"},
        {"id": "2986", "nome": "EGIS - Geofísica TIC H83"},
        {"id": "2987", "nome": "EGIS - Sonsagem e Ensaios LAB - TIC H83"},
        {"id": "2989", "nome": "EGIS - Túnel Botujuru"},
        {"id": "2990", "nome": "EPR - Projeto p/ sinistros de infra rodoviária"},
        {"id": "2991", "nome": "CETENCO - Instrumentação - Estação PT Grande"},
        {"id": "2992", "nome": "Vale Verde - Instrumentação - Mina de Timpopeba"},
        {"id": "2993", "nome": "Vale Verde - Instrumentação e Sondagem - Mina de Timpopeba"},
        {"id": "2995", "nome": "Hydro - Mecânica dos solos e asfalto"},
        {"id": "2996", "nome": "Possebon - Limpeza drenos - DHP-TGB"},
        {"id": "2997", "nome": "EPR - Inspeção OAEs"},
        {"id": "2998", "nome": "EGIS - Sonsagem e Ensaios LAB - 165-2025"},
        {"id": "2999", "nome": "Fazenda Javary - Visita e Inspeção"},
        {"id": "3000", "nome": "ARTEMYN - A2630"},
        {"id": "3001", "nome": "ATERPA - Instrumentação - Barragem Xingu"},
        {"id": "3003", "nome": "EGIS - Alternativa e Projetos de Conteções - BA"},
        {"id": "3004", "nome": "BELOCAL / LHOIST - Investigação Geológica - Matozinhos"},
        {"id": "3005", "nome": "CETENCO - Barragem Igarapeba- São Benedito do Sul"},
        {"id": "3007", "nome": "AGIS - Instrumentação - Metro de SP"},
        {"id": "3008", "nome": "NOVA 381 - Monitoramento de Terrapleno e Conteção"},
        {"id": "3009", "nome": "Projeta - Coleta Denison - Alumar DET2"},
        {"id": "3010", "nome": "RDC 4598558 - Investigação Geotécnica (Campo e Lab.)"},
        {"id": "3011", "nome": "Construcap - Concessão BR-040"},
        {"id": "3012", "nome": "EPR - ParecerBR-277"},
        {"id": "3013", "nome": "EPR - Projeto de Recomposição de Taludes"},
        {"id": "3014", "nome": "Light - Túnel"},
        {"id": "3017", "nome": "EPR - Projeto Executo sinistros infra rodoviaria"},
        {"id": "3018", "nome": "Vale - RC 19923380 Sistemas Estabilização"},
        {"id": "3019", "nome": "NOVA 381 - CCGP 0002_25 CQP e BIM"},
        {"id": "3021", "nome": "Alupar - Investigações Geotécnicas PCH Queluz"},
        {"id": "3022", "nome": "NTS - Leitura Inclinômetros SHAFT GASTAU"},
        {"id": "3023", "nome": "Aterpa - Drenos na PDE União"},
        {"id": "3024", "nome": "Nova 381 - Elaboração de Portfolio de Projetos - Pacote 1"},
        {"id": "3025", "nome": "Nova 381 - Elaboração de Portfolio de Projetos - Pacote 2"},
        {"id": "3026", "nome": "IDP - Barragem Novo Algodões"},
        {"id": "3027", "nome": "Sesc - Sondagem"},
        {"id": "3028", "nome": "Pavidez - Instrumentação - Faixa 5"},
        {"id": "3029", "nome": "NTS - Automação Medidor de Vazão"},
        {"id": "3030", "nome": "ENGEVIX - Plano de instru. da Barragem do Fojo"},
        {"id": "3031", "nome": "IDEP - Barragem Atalaia"},
        {"id": "3032", "nome": "IDEP - Barragem Castelo"},
        {"id": "3033", "nome": "Quanta Consultoria - Parque Linear e Mergulhão"},
        {"id": "3034", "nome": "Lopes Marinho - Novo Campus do IMPA"},
        {"id": "3036", "nome": "FMAC Engenharia - Estudo de Estabilização"},
        {"id": "3037", "nome": "Copasa - Erosões - Divinópolis"},
        {"id": "3038", "nome": "Mosaic Fertilizantes - Sondagem e Instrumentação"},
        {"id": "3039", "nome": "Alumar - RDC 4605963"},
        {"id": "3040", "nome": "Pavidez - Mosaic Fertilizantes"},
        {"id": "3041", "nome": "Light - Sondagens Usinas Hidrelétricas Fontes"},
        {"id": "3042", "nome": "DER-PI - Estudos, Peças e Técnicas e Projetos"},
        {"id": "9010", "nome": "Atividades Internas"},
        {"id": "9012", "nome": "Treinamento"},
        {"id": "9013", "nome": "Marketing"},
        {"id": "9014", "nome": "Propostas"},
        {"id": "9021", "nome": "Férias e Recessos"},
        {"id": "9022", "nome": "Horas Vagas"}
    ]
    
    # Caminho para o arquivo de dados
    arquivo_json = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'dados.json')
    
    # Verificar se o arquivo existe
    if os.path.exists(arquivo_json):
        # Carregar dados existentes
        try:
            with open(arquivo_json, 'r', encoding='utf-8') as f:
                dados = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            dados = {'funcionarios': [], 'projetos': [], 'registros_horas': [], 'usuarios': []}
    else:
        # Inicializar com estrutura vazia
        dados = {'funcionarios': [], 'projetos': [], 'registros_horas': [], 'usuarios': []}
    
    # Obter IDs de projetos existentes
    ids_existentes = set(p['id'] for p in dados.get('projetos', []))
    
    # Adicionar apenas projetos que não existem
    projetos_adicionados = 0
    for projeto in novos_projetos:
        if projeto['id'] not in ids_existentes:
            dados['projetos'].append(projeto)
            ids_existentes.add(projeto['id'])
            projetos_adicionados += 1
    
    # Salvar dados atualizados
    try:
        with open(arquivo_json, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        print(f"Dados salvos com sucesso! {projetos_adicionados} projetos adicionados.")
        return True, projetos_adicionados
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")
        return False, 0

if __name__ == "__main__":
    sucesso, qtd = atualizar_projetos()
    print(f"Atualização {'bem-sucedida' if sucesso else 'falhou'}. {qtd} projetos adicionados.")
