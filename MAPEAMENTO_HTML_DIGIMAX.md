# Mapeamento e Planejamento da Reestruturação HTML para o Estilo Digimax

Este documento detalha o mapeamento dos componentes do template "Digimax" para a estrutura HTML atual do projeto AppTimeSheet e o planejamento para a reestruturação do HTML, visando replicar o design *exatamente igual* ao das imagens fornecidas.

## 1. Estrutura HTML Atual do Projeto

O projeto AppTimeSheet utiliza uma estrutura Flask com Jinja2 para renderização de templates. Os principais arquivos HTML identificados são:

*   `index.html`: Página inicial, contém a estrutura básica da navbar, jumbotron e cards de funcionalidades.
*   `auth/login.html`: Página de login.
*   `funcionarios/listar.html`, `funcionarios/adicionar.html`, `funcionarios/editar.html`.
*   `projetos/listar.html`, `projetos/detalhes.html`.
*   `registros/listar.html`, `registros/adicionar.html`, `registros/editar.html`, `registros/exportar.html`.

Todos esses templates parecem herdar ou incluir uma estrutura comum para a navbar e o footer, além de utilizar o Bootstrap 5 para o layout.

## 2. Mapeamento de Componentes Digimax para o Projeto Atual

Com base na análise visual do template Digimax, os seguintes componentes e seções precisam ser mapeados e adaptados:

| Componente Digimax (Observado nas Imagens) | Componente Equivalente no Projeto Atual | Ações Necessárias para Reestruturação HTML |
| :----------------------------------------- | :-------------------------------------- | :----------------------------------------- |
| **Header/Navbar**                          | `navbar` em `index.html` (e possivelmente em `base.html`) | - Ajustar a estrutura da `navbar` para incluir o logo à esquerda, links de navegação e o botão "GET STARTED" (que pode ser adaptado para "Login" ou "Registrar"). <br> - Garantir que a `navbar` seja consistente em todas as páginas. |
| **Hero Section (seção principal)**         | `jumbotron` em `index.html`             | - Substituir o `jumbotron` por uma seção de herói mais visualmente rica, com título grande, subtítulo e possivelmente uma imagem de fundo ou efeito parallax. <br> - O conteúdo será adaptado para a mensagem de boas-vindas do sistema. |
| **Seções de Conteúdo (Cards)**             | `div.row` com `div.card` em `index.html`, `listar.html`, etc. | - Adaptar a estrutura dos `div.card` para o estilo Digimax (bordas arredondadas, sombras, efeitos de hover). <br> - Organizar os cards em grids responsivos. |
| **Barra Lateral (Sidebar)**                | Não existe diretamente no projeto atual. | - Criar uma estrutura de `sidebar` para páginas de detalhe ou listagem, como visto na página de artigo do Digimax. <br> - Incluir seções como "Categorias Populares" (pode ser adaptado para "Módulos do Sistema"), "Newsletter" (pode ser um formulário de contato ou aviso) e "Posts Recentes" (pode ser adaptado para "Últimos Registros"). |
| **Formulários**                            | `form` em `auth/login.html`, `funcionarios/adicionar.html`, etc. | - Manter a estrutura básica dos formulários, mas aplicar as novas classes CSS para os campos de entrada, labels e botões. <br> - Garantir que os `flash messages` sejam exibidos no novo estilo de alerta. |
| **Tabelas**                                | `table` em `funcionarios/listar.html`, `registros/listar.html`, etc. | - Manter a estrutura básica das tabelas, mas aplicar as novas classes CSS para cabeçalhos, linhas e células. <br> - Garantir bordas arredondadas para a tabela como um todo. |
| **Footer (Rodapé)**                        | `footer` em `index.html` (e possivelmente em `base.html`) | - Reestruturar o `footer` para incluir múltiplas colunas (Serviços, Suporte, Empresa), ícones de redes sociais e informações de direitos autorais, conforme o layout Digimax. |
| **Efeitos Dinâmicos (Parallax)**           | Não existe no projeto atual.            | - Identificar seções onde o efeito parallax pode ser aplicado (ex: Hero Section, seções de fundo). <br> - Adicionar classes e/ou atributos `data-` necessários para a implementação via JavaScript. |

## 3. Planejamento da Reestruturação HTML

Para alcançar a replicação exata do template Digimax, a seguinte abordagem será utilizada:

### 3.1. Criação de um `base.html` Unificado

Será criado um arquivo `src/templates/base.html` que conterá a estrutura HTML comum a todas as páginas, incluindo:

*   `<!DOCTYPE html>`, `<html>`, `<head>` (com meta tags, links para CSS e fontes).
*   A nova estrutura da **Navbar** (Header).
*   O novo **Footer**.
*   Blocos Jinja2 (`{% block content %}` e `{% endblock %}`) para o conteúdo específico de cada página.
*   Links para scripts JavaScript (Bootstrap JS, scripts personalizados, bibliotecas para parallax).

### 3.2. Adaptação dos Templates Existentes

Cada template existente (`index.html`, `auth/login.html`, etc.) será modificado para:

*   Estender o novo `base.html` (`{% extends 
