# Instruções de Uso - Sistema de Controle de Horas com Login

## Visão Geral
O sistema de Controle de Horas foi atualizado com um sistema de login e permissões que diferencia entre funcionários e administradores:

- **Funcionários**: Podem apenas registrar, visualizar e editar suas próprias horas
- **Administradores**: Têm acesso completo a todas as funcionalidades do sistema

## Novos Recursos
- Sistema de login seguro
- Registro de novos usuários com validação de email empresarial (@geoprojetos.com.br)
- Controle de sessão
- Permissões baseadas em perfil de usuário
- Página de perfil para edição de dados pessoais e senha

## Instalação

1. Descompacte o arquivo `controle_horas_login.zip`
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Execute o servidor:
   ```
   python src/main.py
   ```
4. Acesse no navegador: `http://localhost:5000`

## Credenciais Padrão

O sistema vem com um usuário administrador pré-cadastrado:

- **Email**: admin@geoprojetos.com.br
- **Senha**: admin

Recomendamos alterar a senha após o primeiro login.

## Fluxo de Uso

### Para Administradores:
1. Faça login com as credenciais de administrador
2. Acesso completo a todas as funcionalidades:
   - Gerenciar funcionários
   - Visualizar projetos
   - Gerenciar registros de horas de todos os funcionários
   - Exportar relatórios

### Para Funcionários:
1. Registre-se usando email com domínio @geoprojetos.com.br
2. Faça login com suas credenciais
3. Acesso limitado:
   - Registrar suas próprias horas
   - Visualizar seus próprios registros
   - Editar seus próprios registros
   - Visualizar lista de projetos

## Observações Importantes
- Todos os usuários devem usar email com domínio @geoprojetos.com.br
- Cada funcionário só pode ver e editar seus próprios registros
- O sistema cria automaticamente um funcionário associado ao usuário durante o registro
- As senhas são armazenadas de forma segura (hash)

## Suporte
Em caso de dúvidas ou problemas, entre em contato com o administrador do sistema.
