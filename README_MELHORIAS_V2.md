# Sistema de Controle de Horas - Versão Melhorada v2.0

## 🚀 Melhorias Implementadas

### ✅ Nomenclatura Atualizada
- **Funcionários** → **Colaboradores**
- **Projetos** → **Contratos**
- Interface completamente atualizada em todas as páginas

### ✅ Melhorias de UI/UX
- Links de **Perfil** e **Logout** em todas as páginas
- Navegação consistente e intuitiva
- Redirecionamento melhorado após adicionar registros
- Interface responsiva e moderna

### ✅ Cadastro por Lista
- **Importação de Colaboradores** via arquivo Excel
- **Importação de Contratos** via arquivo Excel
- Suporte a IDs customizados (ex: COL001, GP9014)
- Validação e tratamento de erros na importação

### ✅ Registro de Horas Aprimorado
- **Registro Diário**: Para registros específicos por data
- **Registro Mensal**: Para totais mensais por contrato
- Interface com abas para escolher o tipo de registro
- Controle de permissões: funcionários só registram para si mesmos

### ✅ Consulta de Registros Melhorada
- **Visualização Detalhada**: Lista todos os registros individuais
- **Visualização Agregada**: Soma horas por colaborador/contrato/mês
- **Ordenação clicável** por Colaborador, Contrato e Data
- **Totais automáticos** exibidos no rodapé
- Ordem cronológica (mais recentes primeiro)

### ✅ Funcionalidades Mantidas
- Sistema de login e permissões
- Exportação para Excel (múltiplos formatos)
- Relatórios personalizados
- Filtros avançados
- Controle de acesso por tipo de usuário

## 📋 Formato dos Arquivos de Importação

### Colaboradores
```
Coluna A: ID do colaborador (ex: COL001, COL002 ou números)
Coluna B: Nome do colaborador
```

### Contratos
```
Coluna A: ID/GP do contrato (ex: GP9014, GP9010 ou números)
Coluna B: Nome do contrato
```

## 🛠️ Instalação e Uso

1. **Extrair o arquivo:**
   ```bash
   unzip controle_horas_melhorado_v2.zip
   cd controle_horas_melhorado_v2
   ```

2. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Executar o sistema:**
   ```bash
   python src/main.py
   ```

4. **Acessar no navegador:**
   ```
   http://localhost:5000
   ```

## 👤 Login Padrão

- **Email:** admin@geoprojetos.com.br
- **Senha:** admin

## 🌐 Acesso em Rede

Para permitir acesso de outros computadores na mesma rede:

1. Descubra o IP do computador servidor:
   ```bash
   ipconfig  # Windows
   ifconfig  # Linux/Mac
   ```

2. Configure o firewall para permitir conexões na porta 5000

3. Acesse de outros computadores usando:
   ```
   http://[IP_DO_SERVIDOR]:5000
   ```

## 📊 Funcionalidades Principais

- ✅ Cadastro e gestão de colaboradores
- ✅ Gestão de contratos
- ✅ Registro de horas (diário e mensal)
- ✅ Consulta com filtros avançados
- ✅ Visualização detalhada e agregada
- ✅ Exportação para Excel
- ✅ Relatórios personalizados
- ✅ Sistema de permissões
- ✅ Importação por lista (Excel)

## 🔧 Suporte Técnico

Para dúvidas ou problemas, consulte o guia de acesso à rede incluído no pacote anterior ou entre em contato para suporte adicional.

---
**Versão:** 2.0  
**Data:** Junho 2025