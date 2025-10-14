# Detalhamento das Alterações de CSS no Projeto AppTimeSheet (Branch proj-002) - Estilo Digimax

Este documento detalha as modificações extensivas aplicadas ao arquivo CSS principal do projeto AppTimeSheet (`src/static/css/style.css`) para replicar o estilo visual do template "Digimax - Digital Marketing Agency Elementor Pro Template Kit", conforme solicitado. As alterações visam transformar a estética da aplicação para um design mais moderno, escuro e vibrante.

## Sumário das Alterações

As principais modificações realizadas incluem:

*   **Esquema de Cores Digimax**: Implementação de uma paleta de cores escuras com acentos vibrantes (rosa/magenta e laranja).
*   **Tipografia**: Alteração da fonte principal para `Poppins` (ou similar) para um visual mais contemporâneo.
*   **Estilos de Componentes Aprimorados**: Redesenho de elementos como Navbar, Cards, Botões, Formulários, Tabelas e Alertas para se alinharem ao estilo Digimax.
*   **Sombras e Transições**: Uso consistente de sombras e transições suaves para adicionar profundidade e interatividade.
*   **Bordas Arredondadas**: Aplicação de bordas mais arredondadas em diversos componentes para um toque moderno.

## Alterações Detalhadas

### 1. Esquema de Cores e Variáveis CSS

**Localização**: `src/static/css/style.css`

**Descrição da Alteração**: O arquivo `style.css` foi atualizado com um novo conjunto de variáveis CSS (`:root`) para definir um esquema de cores inspirado no template Digimax. A paleta agora inclui tons de roxo escuro para o fundo e elementos secundários, com rosa/magenta e laranja como cores de destaque. O texto foi ajustado para cores claras para garantir contraste e legibilidade em fundos escuros.

**Variáveis CSS Atualizadas**:

```css
:root {
  --primary-dark: #1a0f2d; /* Fundo principal escuro */
  --secondary-dark: #2c1a4b; /* Elementos de fundo secundários */
  --accent-pink: #ff007f; /* Cor de destaque rosa/magenta */
  --accent-orange: #ff8c00; /* Cor de destaque laranja */
  --text-light: #e0e0e0; /* Texto claro */
  --text-dark: #ffffff; /* Texto muito claro para contraste */
  --text-muted: #a0a0a0; /* Texto secundário */
  --border-color: rgba(255, 255, 255, 0.1);
  --border-radius-sm: 0.3rem;
  --border-radius-md: 0.5rem;
  --border-radius-lg: 0.75rem;
  --box-shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.2);
  --box-shadow-md: 0 4px 8px rgba(0, 0, 0, 0.3);
  --transition-ease: all 0.3s ease-in-out;
}
```

### 2. Tipografia

**Localização**: `src/static/css/style.css`

**Descrição da Alteração**: A fonte padrão do corpo do documento foi alterada para `Poppins` (ou uma alternativa sans-serif moderna), que é comumente utilizada em designs contemporâneos, melhorando a legibilidade e a estética geral da aplicação.

**Código Modificado (src/static/css/style.css)**:

```css
body {
  font-family: 'Poppins', sans-serif; /* Ou 'Inter', 'Montserrat' */
  color: var(--text-light);
  background-color: var(--primary-dark);
  line-height: 1.6;
  margin: 0;
  padding: 0;
}
```

### 3. Estilos de Componentes

Diversos componentes da interface foram aprimorados para refletir o design escuro e vibrante do Digimax:

#### Navbar

**Descrição**: A barra de navegação agora possui um fundo `var(--primary-dark)` com uma sombra sutil e uma borda inferior. Os links de navegação têm cores claras e um efeito de hover que muda o fundo para `var(--secondary-dark)`. O link ativo é destacado com `var(--accent-pink)`.

**Código Modificado (src/static/css/style.css)**:

```css
.navbar {
  background-color: var(--primary-dark) !important;
  box-shadow: var(--box-shadow-sm);
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.navbar-brand {
  font-weight: 700;
  font-size: 1.6rem;
  color: var(--text-dark) !important;
}

.navbar-dark .navbar-nav .nav-link {
  color: var(--text-light);
  font-weight: 500;
  padding: 0.6rem 1rem;
  transition: var(--transition-ease);
  border-radius: var(--border-radius-sm);
  margin: 0 0.3rem;
}

.navbar-dark .navbar-nav .nav-link:hover {
  color: var(--text-dark);
  background-color: var(--secondary-dark);
}

.navbar-dark .navbar-nav .nav-link.active {
  color: var(--text-dark);
  background-color: var(--accent-pink);
  box-shadow: var(--box-shadow-sm);
}
```

#### Cards

**Descrição**: Os cards foram estilizados com um fundo `var(--secondary-dark)`, bordas arredondadas maiores (`var(--border-radius-lg)`) e sombras mais proeminentes. Um efeito de elevação (`translateY`) e uma sombra mais intensa foram adicionados ao passar o mouse, conferindo uma sensação de profundidade.

**Código Modificado (src/static/css/style.css)**:

```css
.card {
  background-color: var(--secondary-dark);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--box-shadow-md);
  transition: var(--transition-ease);
  margin-bottom: 2rem;
  overflow: hidden;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
}

.card-header {
  background-color: var(--secondary-dark);
  color: var(--text-dark);
  border-bottom: 1px solid var(--border-color);
  padding: 1.25rem 1.5rem;
  font-weight: 600;
  font-size: 1.2rem;
}

.card-body {
  padding: 2rem;
  color: var(--text-light);
}
```

#### Botões

**Descrição**: Os botões foram redesenhados com cantos arredondados (`var(--border-radius-md)`), texto em maiúsculas e um espaçamento de letras sutil. O botão primário (`.btn-primary`) agora utiliza um gradiente linear com `var(--accent-pink)` e `var(--accent-orange)`, com um efeito de hover que altera a opacidade e eleva o botão.

**Código Modificado (src/static/css/style.css)**:

```css
.btn {
  font-weight: 600;
  padding: 0.8rem 1.8rem;
  border-radius: var(--border-radius-md);
  transition: var(--transition-ease);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: linear-gradient(45deg, var(--accent-pink), var(--accent-orange));
  color: var(--text-dark);
}

.btn-primary:hover {
  opacity: 0.9;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(255, 140, 0, 0.4);
}

.btn-secondary {
  background-color: var(--text-muted);
  color: var(--text-dark);
}

.btn-secondary:hover {
  background-color: #808080;
  transform: translateY(-2px);
}

.btn-success {
  background-color: var(--success-color);
  color: var(--text-dark);
}

.btn-success:hover {
  background-color: #2e7d32;
  transform: translateY(-2px);
}

.btn-danger {
  background-color: var(--danger-color);
  color: var(--text-dark);
}

.btn-danger:hover {
  background-color: #c62828;
  transform: translateY(-2px);
}
```

#### Formulários

**Descrição**: Campos de formulário (`.form-control`, `.form-select`) agora têm um fundo `var(--primary-dark)`, bordas mais definidas e texto claro. O foco visual foi aprimorado com `var(--accent-pink)` e um `box-shadow` correspondente.

**Código Modificado (src/static/css/style.css)**:

```css
.form-control, .form-select {
  background-color: var(--primary-dark);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  padding: 0.75rem 1rem;
  color: var(--text-light);
  transition: var(--transition-ease);
}

.form-control::placeholder {
  color: var(--text-muted);
}

.form-control:focus, .form-select:focus {
  border-color: var(--accent-pink);
  box-shadow: 0 0 0 0.25rem rgba(255, 0, 127, 0.25);
  background-color: var(--secondary-dark);
}

.form-label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text-dark);
}
```

#### Tabelas

**Descrição**: As tabelas foram estilizadas para se integrar ao tema escuro, com fundo `var(--secondary-dark)`, bordas arredondadas e sombras. O cabeçalho da tabela utiliza `var(--primary-dark)` e texto claro. As linhas alternadas e o efeito de hover foram ajustados para melhor contraste e interatividade.

**Código Modificado (src/static/css/style.css)**:

```css
.table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  border-radius: var(--border-radius-md);
  overflow: hidden;
  box-shadow: var(--box-shadow-md);
  background-color: var(--secondary-dark);
}

.table thead th {
  background-color: var(--primary-dark);
  color: var(--text-dark);
  font-weight: 700;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.5px;
  padding: 1rem 1.5rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.table tbody tr {
  border-bottom: 1px solid var(--border-color);
}

.table tbody tr:last-child {
  border-bottom: none;
}

.table tbody tr:nth-child(even) {
  background-color: rgba(0, 0, 0, 0.1);
}

.table tbody tr:hover {
  background-color: rgba(255, 0, 127, 0.1);
}

.table td {
  padding: 1rem 1.5rem;
  vertical-align: middle;
  color: var(--text-light);
}
```

#### Alertas

**Descrição**: Os alertas agora possuem uma borda lateral colorida e um fundo semitransparente que indica o tipo de mensagem, com texto claro para visibilidade em fundos escuros.

**Código Modificado (src/static/css/style.css)**:

```css
.alert {
  border-left: 5px solid;
  border-radius: var(--border-radius-md);
  padding: 1.25rem 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: var(--box-shadow-sm);
  color: var(--text-dark);
}

.alert-success {
  border-color: var(--success-color);
  background-color: rgba(56, 142, 60, 0.2);
}

.alert-danger {
  border-color: var(--danger-color);
  background-color: rgba(211, 47, 47, 0.2);
}

.alert-warning {
  border-color: var(--warning-color);
  background-color: rgba(255, 160, 0, 0.2);
}

.alert-info {
  border-color: var(--info-color);
  background-color: rgba(25, 118, 210, 0.2);
}
```

#### Footer

**Descrição**: O rodapé foi estilizado com um fundo `var(--primary-dark)`, texto `var(--text-muted)` e links `var(--text-light)` com efeito de hover para `var(--accent-pink)`, mantendo a consistência visual com o restante da aplicação.

**Código Modificado (src/static/css/style.css)**:

```css
footer {
  background-color: var(--primary-dark);
  color: var(--text-muted);
  padding: 3rem 0;
  margin-top: 3rem;
  border-top: 1px solid var(--border-color);
}

footer a {
  color: var(--text-light);
  text-decoration: none;
  transition: var(--transition-ease);
}

footer a:hover {
  color: var(--accent-pink);
}

footer .social-icons a {
  font-size: 1.5rem;
  margin-right: 1rem;
}

footer .social-icons a:last-child {
  margin-right: 0;
}
```

## Conclusão

As alterações de CSS implementadas na branch `proj-002` transformam a interface do usuário do AppTimeSheet para um estilo moderno e sofisticado, inspirado no template Digimax. O novo esquema de cores, tipografia e estilos de componentes contribuem para uma experiência visual aprimorada e alinhada às tendências de design atuais.
