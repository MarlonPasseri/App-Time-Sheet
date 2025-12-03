import json
import os

def atualizar_projetos():
    # Lista de projetos do arquivo enviado pelo usuário
    novos_projetos = [
        {"id": 1, "cod": "9010", "nome": "Atividades Internas"},
        {"id": 2, "cod": "9014", "nome": "Propostas"},
        {"id": 3, "cod": "9021", "nome": "Férias e Recessos"},
        {"id": 4, "cod": "656", "nome": "Nexa - Barragem do Peixe"},
        {"id": 5, "cod": "669", "nome": "Nexa - Barragem das Pedras"},
        {"id": 6, "cod": "1796", "nome": "Senac - Instrumentação"},
        {"id": 7, "cod": "1881", "nome": "Enel - Serviços de Consultoria por demandas"},
        {"id": 8, "cod": "1905", "nome": "Ecovix - Instrumentação"},
        {"id": 9, "cod": "1924", "nome": "MRS - Instrumentação Barbacena"},
        {"id": 10, "cod": "2139", "nome": "Heb - Prédio em Campos"},
        {"id": 11, "cod": "2240", "nome": "Enel - Frame Civil"},
        {"id": 12, "cod": "2298", "nome": "Hydro - Instrumentação"},
        {"id": 13, "cod": "2317", "nome": "Comosa - PCH Mosquitão"},
        {"id": 14, "cod": "2339", "nome": "Vale - Manutenção"},
        {"id": 15, "cod": "2359", "nome": "Braskem - Instrumentação Maceió"},
        {"id": 16, "cod": "2396", "nome": "Pavidez - Hydro Fase 3"},
        {"id": 17, "cod": "2400", "nome": "Seel - Coronel Domiciano"},
        {"id": 18, "cod": "2449", "nome": "Alumar - Instrumentação ARB 8 e 9"},
        {"id": 19, "cod": "2510", "nome": "Vale - Consultoria Instrumentação"},
        {"id": 20, "cod": "2516", "nome": "Braskem - Apoio Comite"},
        {"id": 21, "cod": "2548", "nome": "CCR - BR-101 e BR-116"},
        {"id": 22, "cod": "2556", "nome": "NTS - Instrumentação"},
        {"id": 23, "cod": "2565", "nome": "Hydro - Automação"},
        {"id": 24, "cod": "2585", "nome": "Kinfra - KM-217=850 da BR-393RJ"},
        {"id": 25, "cod": "2586", "nome": "Enel - Laranja Doce"},
        {"id": 26, "cod": "2597", "nome": "Puc - Perreira Passos"},
        {"id": 27, "cod": "2602", "nome": "SEFAC - Serra do Fação"},
        {"id": 28, "cod": "2623", "nome": "Vale - Mina do Caue - Itabira"},
        {"id": 29, "cod": "2664", "nome": "Pavidez - Reabilitação DRS 1 - Fase 04"},
        {"id": 30, "cod": "2667", "nome": "EDF - Taludes Serra do Seridó"},
        {"id": 31, "cod": "2678", "nome": "Sefac - Erosões 6 e 73"},
        {"id": 32, "cod": "2704", "nome": "Possebon - Projeto Executivo"},
        {"id": 33, "cod": "2712", "nome": "Vale - Contrato ACG - Instrumentação Convencional"},
        {"id": 34, "cod": "2718", "nome": "Alumar - Investigações Geotécnicas"},
        {"id": 35, "cod": "2747", "nome": "Hydro - Instalação e Automação"},
        {"id": 36, "cod": "2775", "nome": "Ecorodovia - Investigação Geológica"},
        {"id": 37, "cod": "2786", "nome": "EDF - Serra de Seridó Fase II"},
        {"id": 38, "cod": "2857", "nome": "Braskem - Inc - São Miguel dos Campos"},
        {"id": 39, "cod": "2868", "nome": "Const. União Realizações - Instrumentação"},
        {"id": 40, "cod": "2880", "nome": "Alumar - Instrumentação ARB10"},
        {"id": 41, "cod": "2888", "nome": "CIMCOP - Projeto Brucutu"},
        {"id": 42, "cod": "2913", "nome": "Light - Segurança de Barragem"},
        {"id": 43, "cod": "2915", "nome": "Furnas - Campo do Meio"},
        {"id": 44, "cod": "2917", "nome": "PXENERGY - São Mateus do Sul"},
        {"id": 45, "cod": "2919", "nome": "Sesc - Pantanal"},
        {"id": 46, "cod": "2920", "nome": "Ecorodovia - Rio-Minas - Manilha-Magé"},
        {"id": 47, "cod": "2934", "nome": "UFES - Estudo Geotécnico"},
        {"id": 48, "cod": "2942", "nome": "Alumar - Lagoa de Água Bruta"},
        {"id": 49, "cod": "2943", "nome": "MAFRIGEO - Barragens Sertãozinho (SP)"},
        {"id": 50, "cod": "2946", "nome": "Copasa - Monte Carlos"},
        {"id": 51, "cod": "2950", "nome": "NOVA 381 - Concessão BR-381"},
        {"id": 52, "cod": "2952", "nome": "PXENERGY - RISP - São Mateus do Sul"},
        {"id": 53, "cod": "2969", "nome": "Alumar - Sondagem do DET 1"},
        {"id": 54, "cod": "2978", "nome": "EPR - Instrumentação"},
        {"id": 55, "cod": "2982", "nome": "Vale Verde - PDE Cavalo - Fase 1"},
        {"id": 56, "cod": "2983", "nome": "EGIS - Geotecnica e Contenção - BR-101"},
        {"id": 57, "cod": "2985", "nome": "EPR - Levantamento de Campo"},
        {"id": 58, "cod": "2986", "nome": "EGIS - Geofísica TIC H83"},
        {"id": 59, "cod": "2987", "nome": "EGIS - Sonsagem e Ensaios LAB - TIC H83"},
        {"id": 60, "cod": "2989", "nome": "EGIS - Túnel Botujuru"},
        {"id": 61, "cod": "2990", "nome": "EPR - Projeto p/ sinistros de infra rodoviária"},
        {"id": 62, "cod": "2991", "nome": "CETENCO - Instrumentação - Estação PT Grande"},
        {"id": 63, "cod": "2992", "nome": "Vale Verde - Instrumentação - Mina de Timpopeba"},
        {"id": 64, "cod": "2993", "nome": "Vale Verde - Instrumentação e Sondagem - Mina de Timpopeba"},
        {"id": 65, "cod": "2995", "nome": "Hydro - Mecânica dos solos e asfalto"},
        {"id": 66, "cod": "2996", "nome": "Possebon - Limpeza drenos - DHP-TGB"},
        {"id": 67, "cod": "2997", "nome": "EPR - Inspeção OAEs"},
        {"id": 68, "cod": "2998", "nome": "EGIS - Sonsagem e Ensaios LAB - 165-2025"},
        {"id": 69, "cod": "2999", "nome": "Fazenda Javary - Visita e Inspeção"},
        {"id": 70, "cod": "3000", "nome": "ARTEMYN - A2630"},
        {"id": 71, "cod": "3001", "nome": "ATERPA - Instrumentação - Barragem Xingu"},
        {"id": 72, "cod": "3003", "nome": "EGIS - Alternativa e Projetos de Conteções - BA"},
        {"id": 73, "cod": "3004", "nome": "BELOCAL / LHOIST - Investigação Geológica - Matozinhos"},
        {"id": 74, "cod": "3005", "nome": "CETENCO - Barragem Igarapeba- São Benedito do Sul"},
        {"id": 75, "cod": "3007", "nome": "AGIS - Instrumentação - Metro de SP"},
        {"id": 76, "cod": "3008", "nome": "NOVA 381 - Monitoramento de Terrapleno e Conteção"},
        {"id": 77, "cod": "3009", "nome": "Projeta - Coleta Denison - Alumar DET2"},
        {"id": 78, "cod": "3010", "nome": "RDC 4598558 - Investigação Geotécnica (Campo e Lab.)"},
        {"id": 79, "cod": "3011", "nome": "Construcap - Concessão BR-040"},
        {"id": 80, "cod": "3012", "nome": "EPR - ParecerBR-277"},
        {"id": 81, "cod": "3013", "nome": "EPR - Projeto de Recomposição de Taludes"},
        {"id": 82, "cod": "3014", "nome": "Light - Túnel"},
        {"id": 83, "cod": "3017", "nome": "EPR - Projeto Executo sinistros infra rodoviaria"},
        {"id": 84, "cod": "3018", "nome": "Vale - RC 19923380 Sistemas Estabilização"},
        {"id": 85, "cod": "3019", "nome": "NOVA 381 - CCGP 0002_25 CQP e BIM"},
        {"id": 86, "cod": "3021", "nome": "Alupar - Investigações Geotécnicas PCH Queluz"},
        {"id": 87, "cod": "3022", "nome": "NTS - Leitura Inclinômetros SHAFT GASTAU"},
        {"id": 88, "cod": "3023", "nome": "Aterpa - Drenos na PDE União"},
        {"id": 89, "cod": "3024", "nome": "Nova 381 - Elaboração de Portfolio de Projetos - Pacote 1"},
        {"id": 90, "cod": "3025", "nome": "Nova 381 - Elaboração de Portfolio de Projetos - Pacote 2"},
        {"id": 91, "cod": "3026", "nome": "IDP - Barragem Novo Algodões"},
        {"id": 92, "cod": "3027", "nome": "Sesc - Sondagem"},
        {"id": 93, "cod": "3028", "nome": "Pavidez - Instrumentação - Faixa 5"},
        {"id": 94, "cod": "3029", "nome": "NTS - Automação Medidor de Vazão"},
        {"id": 95, "cod": "3030", "nome": "ENGEVIX - Plano de instru. da Barragem do Fojo"},
        {"id": 96, "cod": "3031", "nome": "IDEP - Barragem Atalaia"},
        {"id": 97, "cod": "3032", "nome": "IDEP - Barragem Castelo"},
        {"id": 98, "cod": "3033", "nome": "Quanta Consultoria - Parque Linear e Mergulhão"},
        {"id": 99, "cod": "3034", "nome": "Lopes Marinho - Novo Campus do IMPA"},
        {"id": 100, "cod": "3036", "nome": "FMAC Engenharia - Estudo de Estabilização"},
        {"id": 101, "cod": "3037", "nome": "Copasa - Erosões - Divinópolis"},
        {"id": 102, "cod": "3038", "nome": "Mosaic Fertilizantes - Sondagem e Instrumentação"},
        {"id": 103, "cod": "3039", "nome": "Alumar - RDC 4605963"},
        {"id": 104, "cod": "3040", "nome": "Pavidez - Mosaic Fertilizantes"},
        {"id": 105, "cod": "3041", "nome": "Light - Sondagens Usinas Hidrelétricas Fontes"},
        {"id": 106, "cod": "3042", "nome": "DER-PI - Estudos, Peças e Técnicas e Projetos"},
        {"id": 107, "cod": "9012", "nome": "Treinamento"},
        {"id": 108, "cod": "9013", "nome": "Marketing"},
        {"id": 109, "cod": "9022", "nome": "Horas Vagas"}
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
    # Obter CODs de projetos existentes
    cods_existentes = set(p['cod'] for p in dados.get('projetos', []))
    
    # Adicionar apenas projetos que não existem
    projetos_adicionados = 0
    for projeto in novos_projetos:
        if projeto['id'] not in ids_existentes:
            if projeto['cod'] not in cods_existentes:
                dados['projetos'].append(projeto)
                ids_existentes.add(projeto['id'])
                cods_existentes.add(projeto['cod'])
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
