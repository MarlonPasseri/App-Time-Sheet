import json
import os
import hashlib
import re
from datetime import datetime

class Usuario:
    def __init__(self, id=None, nome=None, email=None, senha_hash=None, tipo="funcionario", cod_funcionario=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.tipo = tipo  # "funcionario" ou "administrador"
        self.cod_funcionario = cod_funcionario  # ID do funcionário
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha_hash': self.senha_hash,
            'tipo': self.tipo,
            'cod_funcionario': self.cod_funcionario,
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            nome=data.get('nome'),
            email=data.get('email'),
            senha_hash=data.get('senha_hash'),
            tipo=data.get('tipo', 'funcionario'),
            cod_funcionario=data.get('cod_funcionario'),
        )
    
    @staticmethod
    def hash_senha(senha):
        """Cria um hash seguro da senha."""
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def verificar_senha(self, senha):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return self.senha_hash == self.hash_senha(senha)
    
    def is_admin(self):
        """Verifica se o usuário é um administrador."""
        return self.tipo == "administrador"
    
    def is_funcionario(self):
        """Verifica se o usuário é um funcionário."""
        return self.tipo == "funcionario"

# Atualizar a classe BancoDeDados para incluir usuários
class BancoDeDados:
    def __init__(self, arquivo_json=None):
        self.arquivo_json = arquivo_json or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'dados.json')
        # self.funcionarios = []
        self.projetos = []
        self.registros_horas = []
        self.usuarios = []
        self.carregar_dados()
        
        # Verificar se existe um administrador, caso contrário, criar um padrão
        if not any(u.is_admin() for u in self.usuarios):
            self._criar_admin_padrao()
    
    def _criar_admin_padrao(self):
        """Cria um usuário administrador padrão se não existir nenhum."""
        admin = Usuario(
            id=1,
            nome="Administrador",
            email="admin@geoprojetos.com.br",
            senha_hash=Usuario.hash_senha("admin"),
            tipo="administrador"
        )
        self.usuarios.append(admin)
        self.salvar_dados()
        print("Administrador padrão criado com sucesso!")
    
    def _carregar_projetos_predefinidos(self):
        """Carrega os projetos predefinidos no sistema."""
        projetos_predefinidos = [
            {"id": 9010, "nome": "Atividades Internas"},
            {"id": 9014, "nome": "Propostas"},
            {"id": 9021, "nome": "Férias e Recessos"}
        ]
        
        for projeto_data in projetos_predefinidos:
            projeto = Projeto(id=projeto_data["id"], nome=projeto_data["nome"])
            self.projetos.append(projeto)
        
        print(f"Carregados {len(projetos_predefinidos)} projetos predefinidos.")
    
    def carregar_dados(self):
        """Carrega os dados do arquivo JSON, se existir."""
        if os.path.exists(self.arquivo_json):
            try:
                with open(self.arquivo_json, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                # self.funcionarios = [Funcionario.from_dict(f) for f in dados.get('funcionarios', [])]
                self.projetos = [Projeto.from_dict(p) for p in dados.get('projetos', [])]
                self.registros_horas = [RegistroHoras.from_dict(r) for r in dados.get('registros_horas', [])]
                self.usuarios = [Usuario.from_dict(u) for u in dados.get('usuarios', [])]
            except Exception as e:
                print(f"Erro ao carregar dados: {e}")
                # Inicializa com listas vazias em caso de erro
                # self.funcionarios = []
                self.projetos = []
                self.registros_horas = []
                self.usuarios = []
        else:
            # Inicializa com listas vazias se o arquivo não existir
            # self.funcionarios = []
            self.projetos = []
            self.registros_horas = []
            self.usuarios = []
            
            # Carrega os projetos pré-definidos
            self._carregar_projetos_predefinidos()
    
    def salvar_dados(self):
        """Salva os dados no arquivo JSON."""
        dados = {
            # 'funcionarios': [f.to_dict() for f in self.funcionarios],
            'projetos': [p.to_dict() for p in self.projetos],
            'registros_horas': [r.to_dict() for r in self.registros_horas],
            'usuarios': [u.to_dict() for u in self.usuarios]
        }
        
        try:
            with open(self.arquivo_json, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            return False
    
    # Métodos para Usuários
    def adicionar_usuario(self, nome, email, senha="12345", tipo="funcionario", cod_funcionario="-"):
        """Adiciona um novo usuário."""
        # --- Validar nome ---
        nome = nome.strip()

        # Regex: precisa de pelo menos duas palavras, só letras (com acentos) e hifens
        padraoNome = r"^[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[-'][A-Za-zÀ-ÖØ-öø-ÿ]+)*\s+[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[-'][A-Za-zÀ-ÖØ-öø-ÿ]+)*(?:\s+[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[-'][A-Za-zÀ-ÖØ-öø-ÿ]+)*)*$"

        if not re.match(padraoNome, nome):
            return None, "O nome deve conter no mínimo nome e sobrenome, sem números ou símbolos."

        # --- Validar email empresarial ---
        email = email.strip()

        if not re.match(r"[^@]+@geoprojetos\.com\.br$", email):
            return None, "Email deve ser do domínio @geoprojetos.com.br"
        
        # Verificar se o email já está em uso
        if any(u.email == email for u in self.usuarios):
            return None, f"O email <strong>{email}</strong> já está em uso"
        
        # --- Validar código do funcionário ---
        if cod_funcionario != "-":
            cod_funcionario = cod_funcionario.strip()

            # Verificar se o código já está em uso por outro usuário
            if any(u.cod_funcionario == cod_funcionario for u in self.usuarios):
                return None, f"O código <strong>{cod_funcionario}</strong> já está em uso"
        
        # Gera um novo ID (maior ID existente + 1)
        novo_id = 1
        if self.usuarios:
            novo_id = max(u.id for u in self.usuarios if u.id is not None) + 1
        
        # --- Validar senha ---
        if senha != "12345":
            senha = senha.strip()

            # Mínimo 8 caracteres, 1 maiúscula e 1 símbolo
            padraoSenha = r"^(?=.*[A-Z])(?=.*[^A-Za-z0-9]).{8,}$"

            if not re.match(padraoSenha, senha):
                return None, f"A senha deve conter no mínimo 8 caracteres, pelo menos uma letra maiúscula e pelo menos um símbolo."
        
        # --- Criar hash da senha ---
        senha_hash = Usuario.hash_senha(senha)
        
        usuario = Usuario(
            id=novo_id,
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            tipo=tipo,
            cod_funcionario=cod_funcionario
        )
        
        self.usuarios.append(usuario)
        self.salvar_dados()
        return usuario, "Usuário criado com sucesso"
    
    def autenticar_usuario(self, email, senha):
        """Autentica um usuário com email e senha."""
        for usuario in self.usuarios:
            if usuario.email == email and usuario.verificar_senha(senha):
                return usuario
        return None
    
    def obter_usuario(self, id):
        """Obtém um usuário pelo ID."""
        for usuario in self.usuarios:
            if usuario.id == id:
                return usuario
        return None
    
    def obter_usuario_por_email(self, email):
        """Obtém um usuário pelo email."""
        for usuario in self.usuarios:
            if usuario.email == email:
                return usuario
        return None
    
    def listar_usuarios(self):
        """Lista todos os usuários."""
        return self.usuarios
    
    def atualizar_usuario(self, id, nome=None, email=None, senha=None, tipo=None, cod_funcionario="-"):
        """Atualiza um usuário existente."""
        usuario = self.obter_usuario(id)
        if not usuario:
            return False, "Usuário não encontrado"
        
        if nome:
            # Validar nome
            nome = nome.strip()

            # Regex: precisa de pelo menos duas palavras, só letras (com acentos) e hifens
            padrao = r"^[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[-'][A-Za-zÀ-ÖØ-öø-ÿ]+)*\s+[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[-'][A-Za-zÀ-ÖØ-öø-ÿ]+)*(?:\s+[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[-'][A-Za-zÀ-ÖØ-öø-ÿ]+)*)*$"

            if not re.match(padrao, nome):
                return False, "O nome deve conter no mínimo nome e sobrenome, sem números ou símbolos."
            
            usuario.nome = nome
        
        if email:
            email = email.strip()

            # Validar email empresarial
            if not re.match(r"[^@]+@geoprojetos\.com\.br$", email):
                return False, "Email deve ser do domínio @geoprojetos.com.br"
            
            # Verificar se o email já está em uso por outro usuário
            for u in self.usuarios:
                if u.id != id and u.email == email:
                    return False, f"O email <strong>{email}</strong> já está em uso"
            
            usuario.email = email
        
        if senha:
            # --- Validar senha ---
            senha = senha.strip()

            # Mínimo 8 caracteres, 1 maiúscula e 1 símbolo
            padraoSenha = r"^(?=.*[A-Z])(?=.*[^A-Za-z0-9]).{8,}$"

            if not re.match(padraoSenha, senha):
                return False, f"A senha deve conter no mínimo 8 caracteres, pelo menos uma letra maiúscula e pelo menos um símbolo."
            usuario.senha_hash = Usuario.hash_senha(senha)
        
        if tipo:
            usuario.tipo = tipo
        
        if cod_funcionario != "-":
            cod_funcionario = cod_funcionario.strip()

            # Verificar se o código já está em uso por outro usuário
            for u in self.usuarios:
                if u.id != id and u.cod_funcionario == cod_funcionario:
                    return False, f"O código <strong>{cod_funcionario}</strong> já está em uso"
            usuario.cod_funcionario = cod_funcionario
        
        self.salvar_dados()
        return True, "Usuário atualizado com sucesso"
    
    def remover_usuario(self, id):
        """Remove um usuário pelo ID."""
        usuario = self.obter_usuario(id)
        if usuario:
            self.usuarios.remove(usuario)
            self.salvar_dados()
            return True
        return False
    
    # Métodos para Registros de Horas com controle de acesso
    def listar_registros_horas_por_usuario(self, usuario_id, funcionario_id=None, projeto_id=None, mes_ano=None):
        """
        Lista registros de horas com filtros opcionais e controle de acesso.
        
        Args:
            usuario_id: ID do usuário que está fazendo a consulta
            funcionario_id: Filtrar por ID do funcionário (opcional)
            projeto_id: Filtrar por ID do projeto (opcional)
            mes_ano: Filtrar por mês/ano no formato "YYYY-MM" (opcional)
        
        Returns:
            Lista de registros filtrados com base nas permissões do usuário
        """
        usuario = self.obter_usuario(usuario_id)
        if not usuario:
            return []
        
        # Se for administrador, pode ver todos os registros (com filtros opcionais)
        if usuario.is_admin():
            return self.listar_registros_horas(funcionario_id, projeto_id, mes_ano)
        
        # Se for funcionário, só pode ver seus próprios registros
        if usuario.is_funcionario() and usuario.funcionario_id:
            # Forçar o filtro pelo ID do funcionário associado ao usuário
            registros_filtrados = [r for r in self.registros_horas if r.funcionario_id == usuario.funcionario_id]
            
            # Aplicar filtros adicionais
            if projeto_id is not None:
                registros_filtrados = [r for r in registros_filtrados if r.projeto_id == projeto_id]
            
            if mes_ano is not None:
                registros_filtrados = [r for r in registros_filtrados if r.mes_ano_referencia == mes_ano]
            
            return registros_filtrados
        
        # Se não tiver permissão ou não for associado a um funcionário
        return []
    
    def adicionar_registro_horas_por_usuario(self, usuario_id, projeto_id, data, horas_trabalhadas):
        """Adiciona um novo registro de horas com controle de acesso."""
        usuario = self.obter_usuario(usuario_id)
        if not usuario:
            return None, "Usuário não encontrado"
        
        # Se for administrador, pode adicionar para qualquer funcionário
        if usuario.is_admin():
            # Neste caso, o administrador precisa especificar o funcionário_id em outra função
            return None, "Administrador deve usar a função específica para adicionar registros"
        
        # Se for funcionário, só pode adicionar para si mesmo
        if usuario.is_funcionario() and usuario.funcionario_id:
            funcionario_id = usuario.funcionario_id
            registro = self.adicionar_registro_horas(funcionario_id, projeto_id, data, horas_trabalhadas)
            if registro:
                return registro, "Registro adicionado com sucesso"
            else:
                return None, "Erro ao adicionar registro"
        
        return None, "Usuário sem permissão ou não associado a um funcionário"
    
    def editar_registro_horas_por_usuario(self, usuario_id, registro_id, projeto_id=None, data=None, horas_trabalhadas=None):
        """Edita um registro de horas com controle de acesso."""
        usuario = self.obter_usuario(usuario_id)
        if not usuario:
            return False, "Usuário não encontrado"
        
        registro = self.obter_registro_horas(registro_id)
        if not registro:
            return False, "Registro não encontrado"
        
        # Se for administrador, pode editar qualquer registro
        if usuario.is_admin():
            if self.atualizar_registro_horas(registro_id, None, projeto_id, data, horas_trabalhadas):
                return True, "Registro atualizado com sucesso"
            else:
                return False, "Erro ao atualizar registro"
        
        # Se for funcionário, só pode editar seus próprios registros
        if usuario.is_funcionario() and usuario.funcionario_id:
            if registro.funcionario_id != usuario.funcionario_id:
                return False, "Sem permissão para editar este registro"
            
            # Não permitir alterar o funcionário associado ao registro
            if self.atualizar_registro_horas(registro_id, None, projeto_id, data, horas_trabalhadas):
                return True, "Registro atualizado com sucesso"
            else:
                return False, "Erro ao atualizar registro"
        
        return False, "Usuário sem permissão ou não associado a um funcionário"
    
    def remover_registro_horas_por_usuario(self, usuario_id, registro_id):
        """Remove um registro de horas com controle de acesso."""
        usuario = self.obter_usuario(usuario_id)
        if not usuario:
            return False, "Usuário não encontrado"
        
        registro = self.obter_registro_horas(registro_id)
        if not registro:
            return False, "Registro não encontrado"
        
        # Se for administrador, pode remover qualquer registro
        if usuario.is_admin():
            if self.remover_registro_horas(registro_id):
                return True, "Registro removido com sucesso"
            else:
                return False, "Erro ao remover registro"
        
        # Se for funcionário, só pode remover seus próprios registros
        if usuario.is_funcionario() and usuario.funcionario_id:
            if registro.funcionario_id != usuario.funcionario_id:
                return False, "Sem permissão para remover este registro"
            
            if self.remover_registro_horas(registro_id):
                return True, "Registro removido com sucesso"
            else:
                return False, "Erro ao remover registro"
        
        return False, "Usuário sem permissão ou não associado a um funcionário"
    
    # Métodos para Funcionários
    def adicionar_funcionario(self, nome):
        """Adiciona um novo funcionário."""
        # Gera um novo ID (maior ID existente + 1)
        novo_id = 1
        if self.funcionarios:
            novo_id = max(f.id for f in self.funcionarios if f.id is not None) + 1
        
        funcionario = Funcionario(id=novo_id, nome=nome)
        self.funcionarios.append(funcionario)
        self.salvar_dados()
        return funcionario
    
    def obter_funcionario(self, id):
        """Obtém um funcionário pelo ID."""
        for funcionario in self.funcionarios:
            if funcionario.id == id:
                return funcionario
        return None
    
    def listar_funcionarios(self):
        """Lista todos os funcionários."""
        return self.funcionarios
    
    def atualizar_funcionario(self, id, nome):
        """Atualiza um funcionário existente."""
        funcionario = self.obter_funcionario(id)
        if funcionario:
            funcionario.nome = nome
            self.salvar_dados()
            return True
        return False
    
    def remover_funcionario(self, id):
        """Remove um funcionário pelo ID."""
        funcionario = self.obter_funcionario(id)
        if funcionario:
            self.funcionarios.remove(funcionario)
            self.salvar_dados()
            return True
        return False
    
    # Métodos para Projetos
    def adicionar_projeto(self, nome):
        """Adiciona um novo projeto."""
        # Gera um novo ID (maior ID existente + 1)
        novo_id = 1
        if self.projetos:
            novo_id = max(p.id for p in self.projetos if p.id is not None) + 1
        
        projeto = Projeto(id=novo_id, nome=nome)
        self.projetos.append(projeto)
        self.salvar_dados()
        return projeto
    
    def obter_projeto(self, id):
        """Obtém um projeto pelo ID."""
        for projeto in self.projetos:
            if projeto.id == id:
                return projeto
        return None
    
    def listar_projetos(self):
        """Lista todos os projetos."""
        return self.projetos
    
    def atualizar_projeto(self, id, nome):
        """Atualiza um projeto existente."""
        projeto = self.obter_projeto(id)
        if projeto:
            projeto.nome = nome
            self.salvar_dados()
            return True
        return False
    
    def remover_projeto(self, id):
        """Remove um projeto pelo ID."""
        projeto = self.obter_projeto(id)
        if projeto:
            self.projetos.remove(projeto)
            self.salvar_dados()
            return True
        return False
    
    # Métodos para Registros de Horas
    def adicionar_registro_horas(self, funcionario_id, projeto_id, data, horas_trabalhadas):
        """Adiciona um novo registro de horas."""
        # Verifica se o funcionário e o projeto existem
        funcionario = self.obter_usuario(funcionario_id)
        projeto = self.obter_projeto(projeto_id)
        if not funcionario or not projeto:
            return None
        
        # Gera um novo ID (maior ID existente + 1)
        novo_id = 1
        if self.registros_horas:
            novo_id = max(r.id for r in self.registros_horas if r.id is not None) + 1
        
        registro = RegistroHoras(
            id=novo_id,
            funcionario_id=funcionario_id,
            projeto_id=projeto_id,
            data=data,
            horas_trabalhadas=horas_trabalhadas
        )
        self.registros_horas.append(registro)
        self.salvar_dados()
        return registro
    
    def obter_registro_horas(self, id):
        """Obtém um registro de horas pelo ID."""
        for registro in self.registros_horas:
            if registro.id == id:
                return registro
        return None
    
    def listar_registros_horas(self, funcionario_id=None, projeto_id=None, mes_ano=None):
        """Lista registros de horas com filtros opcionais."""
        registros_filtrados = self.registros_horas
        
        if funcionario_id is not None:
            registros_filtrados = [r for r in registros_filtrados if r.funcionario_id == funcionario_id]
        
        if projeto_id is not None:
            registros_filtrados = [r for r in registros_filtrados if r.projeto_id == projeto_id]
        
        if not mes_ano:  # trata "", None, " "
            mes_ano = None

        if mes_ano is not None:
            registros_filtrados = [r for r in registros_filtrados if r.data == datetime.strptime(mes_ano, "%Y-%m").strftime("%m-%Y")]
        
        return registros_filtrados
    
    def atualizar_registro_horas(self, id, funcionario_id=None, projeto_id=None, data=None, horas_trabalhadas=None):
        """Atualiza um registro de horas existente."""
        registro = self.obter_registro_horas(id)
        if not registro:
            return False
        
        if funcionario_id is not None:
            funcionario = self.obter_usuario(funcionario_id)
            if not funcionario:
                return False
            registro.funcionario_id = funcionario_id
        
        if projeto_id is not None:
            projeto = self.obter_projeto(projeto_id)
            if not projeto:
                return False
            registro.projeto_id = projeto_id
        
        if data is not None:
            registro.data = data
            # Atualizar o mês/ano de referência
            # if isinstance(data, str):
            #     data_obj = datetime.strptime(data, "%Y-%m")
            #     # registro.mes_ano_referencia = data_obj.strftime("%Y-%m")
            #     registro.data = data_obj.strftime("%m-%Y")
            # elif isinstance(data, datetime):
            #     # registro.mes_ano_referencia = data.strftime("%Y-%m")
            #     registro.data = data.strftime("%m-%Y")
        
        if horas_trabalhadas is not None:
            registro.horas_trabalhadas = horas_trabalhadas
        
        self.salvar_dados()
        return True
    
    def remover_registro_horas(self, id):
        """Remove um registro de horas pelo ID."""
        registro = self.obter_registro_horas(id)
        if registro:
            self.registros_horas.remove(registro)
            self.salvar_dados()
            return True
        return False

# Manter as classes existentes
# class Funcionario:
#     def __init__(self, id=None, nome=None):
#         self.id = id
#         self.nome = nome
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'nome': self.nome
#         }
    
#     @classmethod
#     def from_dict(cls, data):
#         return cls(id=data.get('id'), nome=data.get('nome'))

class Projeto:
    def __init__(self, id=None, nome=None):
        self.id = id
        self.nome = nome
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(id=data.get('id'), nome=data.get('nome'))

class RegistroHoras:
    def __init__(self, id=None, funcionario_id=None, projeto_id=None, data=None, horas_trabalhadas=None):
        self.id = id
        self.funcionario_id = funcionario_id
        self.projeto_id = projeto_id
        self.data = data
        self.horas_trabalhadas = horas_trabalhadas
        
        # Calcular o mês/ano de referência automaticamente
        # if isinstance(data, str):
        #     data_obj = datetime.strptime(data, "%Y-%m-%d")
        #     self.mes_ano_referencia = data_obj.strftime("%Y-%m")
        # elif isinstance(data, datetime):
        #     self.mes_ano_referencia = data.strftime("%Y-%m")
        # else:
        #     self.mes_ano_referencia = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'funcionario_id': self.funcionario_id,
            'projeto_id': self.projeto_id,
            'data': self.data,
            'horas_trabalhadas': self.horas_trabalhadas,
            # 'mes_ano_referencia': self.mes_ano_referencia
        }
    
    @classmethod
    def from_dict(cls, data):
        registro = cls(
            id=data.get('id'),
            funcionario_id=data.get('funcionario_id'),
            projeto_id=data.get('projeto_id'),
            data=data.get('data'),
            horas_trabalhadas=data.get('horas_trabalhadas')
        )
        # if 'mes_ano_referencia' in data:
        #     registro.mes_ano_referencia = data.get('mes_ano_referencia')
        return registro
