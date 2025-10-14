# Detalhamento das Alterações no Projeto AppTimeSheet (Branch proj-002)

Este documento detalha as melhorias e correções de erros implementadas no projeto AppTimeSheet, resultando na criação da branch `proj-002`. As alterações visam aprimorar a segurança, a robustez e a organização do código.

## Sumário das Alterações

As principais modificações realizadas incluem:

*   **Melhoria na Segurança de Senhas**: Substituição do método de hashing de senhas por uma abordagem mais robusta utilizando `werkzeug.security`.
*   **Refatoração e Limpeza de Código**: Remoção de arquivos e importações não utilizados que causavam confusão e não estavam integrados ao fluxo principal da aplicação.
*   **Controle de Acesso Aprimorado**: Aplicação de decoradores de autenticação (`@login_required`) e autorização (`@admin_required`) em rotas críticas para garantir que apenas usuários autorizados possam acessar ou modificar recursos.
*   **Geração de IDs Únicos para Usuários**: Implementação de um método mais seguro e confiável para a geração de IDs de usuário, evitando possíveis conflitos.

## Alterações Detalhadas

### 1. Melhoria na Segurança de Senhas

**Localização**: `src/models/models.py`

**Descrição da Alteração**: Anteriormente, o projeto utilizava `hashlib.sha256` para fazer o hash das senhas, o que é considerado inseguro para armazenamento de senhas, pois não inclui um *salt* e é vulnerável a ataques de *rainbow table*. Para corrigir isso, a implementação foi atualizada para usar `generate_password_hash` e `check_password_hash` do módulo `werkzeug.security`. Esta é uma prática recomendada para o armazenamento seguro de senhas em aplicações Flask.

**Código Modificado (src/models/models.py)**:

```python
# Antes:
import hashlib
...
class Usuario:
    ...
    @staticmethod
    def hash_senha(senha):
        return hashlib.sha256(senha.encode()).hexdigest()

    def verificar_senha(self, senha):
        return self.senha_hash == self.hash_senha(senha)

# Depois:
from werkzeug.security import generate_password_hash, check_password_hash
...
class Usuario:
    ...
    @staticmethod
    def hash_senha(senha):
        return generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
```

### 2. Refatoração e Limpeza de Código

**Localização**: `src/routes/user.py`, `src/models/user.py`, `src/main.py`

**Descrição da Alteração**: Foi identificado que os arquivos `src/routes/user.py` e `src/models/user.py` não estavam sendo utilizados ou estavam relacionados a uma implementação alternativa de gerenciamento de usuários que não estava integrada ao fluxo principal do projeto. Para evitar código morto e confusão, esses arquivos foram removidos. Consequentemente, as importações relacionadas a eles em `src/main.py` também foram removidas.

**Ações Realizadas**:
*   Remoção de `/home/ubuntu/project/CONTROLE-DE-HORAS-V.2-main/src/routes/user.py`
*   Remoção de `/home/ubuntu/project/CONTROLE-DE-HORAS-V.2-main/src/models/user.py`
*   Remoção de importações de `user_bp` em `src/main.py`.

### 3. Controle de Acesso Aprimorado

**Localização**: `src/routes/registros.py`, `src/routes/funcionarios.py`, `src/routes/projetos.py`

**Descrição da Alteração**: Decoradores de autenticação (`@login_required`) e autorização (`@admin_required`) foram aplicados a várias rotas para garantir que apenas usuários logados e/ou administradores possam acessar funcionalidades específicas. Isso aumenta significativamente a segurança da aplicação, prevenindo acessos não autorizados.

**Rotas Afetadas e Alterações Específicas**:

*   **`src/routes/registros.py`**:
    *   `@registros_bp.route('/adicionar')`: Adicionado `@login_required`.
    *   `@registros_bp.route('/editar/<int:id>')`: Adicionado `@login_required`.
    *   `@registros_bp.route('/remover/<int:id>')`: Adicionado `@login_required`.
    *   `@registros_bp.route('/exportar')`: Adicionado `@login_required`.
    *   `@registros_bp.route('/exportar/excel')`: Adicionado `@login_required`.
    *   A função `db.listar_registros_horas` agora recebe `usuario_id` para aplicar filtros de permissão adequados.

*   **`src/routes/funcionarios.py`**:
    *   `@funcionarios_bp.route('/remover/<int:id>')`: Adicionado `@admin_required`.
    *   `@funcionarios_bp.route('/api/listar')`: Adicionado `@login_required`.

*   **`src/routes/projetos.py`**:
    *   `@projetos_bp.route('/api/listar')`: Adicionado `@login_required`.
    *   Correção de importação duplicada de `login_required` e `admin_required`.

### 4. Geração de IDs Únicos para Usuários

**Localização**: `src/models/models.py`

**Descrição da Alteração**: Para garantir a unicidade e a robustez na atribuição de IDs para novos usuários, um novo método `_gerar_novo_id_usuario()` foi implementado na classe `BancoDeDados`. Este método garante que o ID gerado seja sempre o maior ID existente + 1, mesmo que haja lacunas nos IDs existentes, evitando colisões e facilitando o gerenciamento de usuários.

**Código Modificado (src/models/models.py)**:

```python
# Adição do método:
class BancoDeDados:
    ...
    def _gerar_novo_id_usuario(self):
        """Gera um novo ID único para usuários."""
        if not self.usuarios:
            return 1
        return max(u.id for u in self.usuarios if u.id is not None) + 1

# Uso na função adicionar_usuario:
    def adicionar_usuario(self, nome, email, senha, tipo="funcionario", funcionario_id=None):
        ...
        novo_id = self._gerar_novo_id_usuario()
        ...

# Uso na função _criar_admin_padrao:
    def _criar_admin_padrao(self):
        ...
        admin = Usuario(
            id=self._gerar_novo_id_usuario(),
            ...
        )
        ...
```

## Conclusão

As alterações implementadas na branch `proj-002` do projeto AppTimeSheet abordam questões críticas de segurança e organização do código, tornando a aplicação mais segura e fácil de manter. A melhoria no tratamento de senhas, o controle de acesso mais rigoroso e a gestão aprimorada de IDs de usuário contribuem para um sistema mais confiável e profissional.
