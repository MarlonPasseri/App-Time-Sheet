## Remodelação Completa do Site - Estilo Digimax (Branch `proj-002`)

Esta documentação detalha as alterações extensivas realizadas no projeto para replicar o estilo visual e interativo do template "Digimax - Digital Marketing Agency Elementor Pro Template Kit", conforme solicitado. As modificações abrangeram a estrutura HTML, o estilo CSS e a adição de funcionalidades JavaScript para efeitos dinâmicos.

### 1. Reestruturação HTML

A principal alteração na estrutura HTML foi a introdução de um arquivo `base.html` para centralizar elementos comuns a todas as páginas, como o cabeçalho (navbar) e o rodapé (footer). Todos os outros arquivos HTML foram modificados para estender este `base.html`, garantindo consistência e facilitando a manutenção.

**Arquivos HTML Modificados:**

*   `src/templates/base.html`: **Novo arquivo.** Criado para definir a estrutura básica do site, incluindo:
    *   Uma `navbar` moderna e responsiva com links de navegação e botões de login/logout/perfil.
    *   Um `footer` estilizado com informações de copyright e links sociais.
    *   Blocos `{% block title %}` e `{% block content %}` para que as páginas filhas possam injetar seu conteúdo específico.
*   `src/templates/index.html`: Adaptado para estender `base.html` e incluir um layout de cards e seções de conteúdo que refletem o design do template Digimax.
*   `src/templates/auth/login.html`, `src/templates/auth/perfil.html`, `src/templates/auth/registro.html`: Reestruturados para estender `base.html` e ter seus formulários e conteúdos adaptados ao novo estilo, removendo estilos e estruturas HTML redundantes que estavam presentes.
*   `src/templates/funcionarios/adicionar.html`, `src/templates/funcionarios/editar.html`, `src/templates/funcionarios/listar.html`: Adaptados para estender `base.html`. Os formulários e tabelas foram ajustados para se integrarem ao novo design.
*   `src/templates/projetos/adicionar.html`, `src/templates/projetos/editar.html`, `src/templates/projetos/detalhes.html`, `src/templates/projetos/listar.html`: Reestruturados para estender `base.html`. Os formulários, tabelas e detalhes de projetos foram atualizados para o novo visual.
*   `src/templates/registros/adicionar.html`, `src/templates/registros/editar.html`, `src/templates/registros/exportar.html`, `src/templates/registros/listar.html`: Adaptados para estender `base.html`. Os formulários de registro, tabelas e opções de exportação foram integrados ao novo design.

### 2. Estilo CSS Detalhado (`src/static/css/style.css`)

O arquivo `style.css` foi completamente reescrito para emular o estilo visual do template Digimax. As principais características implementadas incluem:

*   **Variáveis CSS:** Definição de um conjunto abrangente de variáveis para cores, fontes, espaçamentos, sombras, gradientes e transições, facilitando a consistência e futuras modificações.
*   **Esquema de Cores:** Utilização de um esquema de cores vibrante com roxos e rosas (`--color-primary`, `--color-secondary`, `--color-accent-pink`, `--color-accent-purple`) sobre fundos escuros (`--color-bg-dark`, `--color-bg-darker`, `--color-bg-card`).
*   **Tipografia:** Aplicação da fonte 'Inter' (ou similar) com pesos variados para títulos e corpo de texto, buscando clareza e modernidade.
*   **Navbar:** Estilização da barra de navegação com fundo semitransparente (`backdrop-filter`), efeito de `scroll` para adicionar sombra e transições suaves nos links.
*   **Botões:** Design de botões com gradientes, sombras sutis e efeitos de `hover` para uma experiência mais interativa.
*   **Cards:** Estilo de cards com bordas arredondadas, sombras e efeitos de `hover` para indicar interatividade.
*   **Formulários:** Campos de formulário estilizados para se integrarem ao tema escuro, com foco visual claro ao serem selecionados.
*   **Tabelas:** Tabelas com design limpo, linhas alternadas e efeitos de `hover` para melhorar a legibilidade.
*   **Alertas:** Estilização de mensagens de alerta com cores e ícones consistentes com o tema.
*   **Rodapé:** Rodapé com fundo escuro, links sociais e informações de copyright.
*   **Responsividade:** Ajustes básicos para garantir que o layout se adapte a diferentes tamanhos de tela.
*   **Efeitos Especiais:** Inclusão de classes para efeitos como `glow-effect`, `gradient-text` e `glass-effect` para elementos específicos.

### 3. Efeitos Dinâmicos e Interatividade JavaScript (`src/static/js/script.js`)

O arquivo `script.js` foi atualizado para incluir diversas funcionalidades interativas e efeitos dinâmicos, buscando replicar a experiência do usuário do template Digimax:

*   **Navbar Scroll Effect:** Adiciona uma classe `scrolled` à navbar quando o usuário rola a página, alterando seu estilo (ex: adicionando sombra).
*   **Smooth Scroll:** Implementa rolagem suave para links de âncora (`a[href^="#"]`).
*   **Animação de Fade In ao Scroll:** Elementos como cards e tabelas aparecem com um efeito de `fade-in` e `slide-up` quando entram na viewport, usando `IntersectionObserver`.
*   **Parallax Effect:** Adiciona um efeito de parallax a elementos com o atributo `data-parallax`, movendo-os em uma velocidade diferente do scroll da página.
*   **Tooltips do Bootstrap:** Inicialização de tooltips para elementos com `data-bs-toggle="tooltip"`.
*   **Confirmação de Exclusão:** Mensagens de confirmação aprimoradas para botões de exclusão.
*   **Filtros Dinâmicos para Tabelas:** Lógica para filtrar linhas de tabelas com base em inputs de texto.
*   **Animação de Hover nos Cards:** Efeitos de transformação (`translateY`, `scale`) ao passar o mouse sobre os cards.
*   **Loading Spinner para Formulários:** Adiciona um spinner e desabilita o botão de submit durante o processamento do formulário.
*   **Auto-hide Alerts:** Mensagens de alerta desaparecem automaticamente após um tempo, exceto as permanentes.
*   **Contador Animado:** Implementação de um contador que anima o número de zero ao valor alvo ao entrar na viewport.
*   **Validação de Formulários:** Feedback visual para campos de formulário obrigatórios.
*   **Datepickers:** Ajustes para campos de data.
*   **Toggle de Visualização:** Funcionalidade para alternar a visibilidade de elementos.
*   **Copy to Clipboard:** Botões com funcionalidade de copiar texto para a área de transferência.
*   **Mobile Menu Toggle:** Lógica para o funcionamento do menu de navegação em dispositivos móveis.
*   **Tabela Responsiva:** Garante que as tabelas sejam responsivas, envolvendo-as em um `div.table-responsive`.
*   **Loading State para Botões:** Botões com texto de carregamento personalizado.
*   **Dark Mode Toggle (Opcional):** Estrutura para um futuro toggle de modo escuro.
*   **Inicialização de Modals:** Lógica para inicializar e exibir modais do Bootstrap.
*   **Preloader (se existir):** Lógica para ocultar um preloader após o carregamento da página.
*   **Back to Top Button:** Botão para rolar a página de volta ao topo.
*   **Utilitários Globais:** Funções auxiliares para formatação de moeda, data e debounce/throttle.

### Conclusão

Esta remodelação buscou transformar completamente a interface do usuário do projeto para alinhar-se ao estilo moderno e dinâmico do template Digimax. A combinação de uma estrutura HTML bem definida, um CSS detalhado e JavaScript interativo proporciona uma experiência de usuário rica e visualmente atraente. Recomenda-se testar a aplicação em diferentes navegadores e dispositivos para garantir a consistência do design e a funcionalidade de todos os efeitos.
