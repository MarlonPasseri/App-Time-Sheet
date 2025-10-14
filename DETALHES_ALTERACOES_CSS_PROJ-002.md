# Detalhamento das Alterações de CSS no Projeto AppTimeSheet (Branch proj-002)

Este documento detalha as melhorias e modernizações aplicadas ao arquivo CSS principal do projeto AppTimeSheet, resultando na atualização da branch `proj-002`. As alterações visam proporcionar uma experiência de usuário mais agradável e moderna.

## Sumário das Alterações

As principais modificações realizadas incluem:

*   **Esquema de Cores Atualizado**: Introdução de um novo esquema de cores mais vibrante e profissional.
*   **Tipografia Aprimorada**: Utilização da fonte 'Roboto' para uma leitura mais limpa e moderna.
*   **Estilos de Componentes Modernizados**: Melhorias visuais em elementos como Navbar, Cards, Botões, Formulários, Tabelas e Alertas.
*   **Sombras e Transições Suaves**: Adição de sombras e transições para criar um efeito de profundidade e interatividade.

## Alterações Detalhadas

### 1. Esquema de Cores e Variáveis CSS

**Localização**: `src/static/css/style.css`

**Descrição da Alteração**: O arquivo `style.css` foi atualizado com um novo conjunto de variáveis CSS (`:root`) para definir um esquema de cores mais moderno e consistente. As cores primárias e secundárias foram alteradas para tons de azul e roxo, com uma cor de destaque laranja, proporcionando um visual mais contemporâneo.

**Variáveis CSS Atualizadas**:

```css
:root {
  --primary-color: #1a237e; /* Azul escuro */
  --secondary-color: #5c6bc0; /* Azul médio */
  --accent-color: #ffab40; /* Laranja vibrante */
  --light-bg: #f5f5f5; /* Fundo claro */
  --dark-text: #212121; /* Texto escuro */
  --light-text: #ffffff; /* Texto claro */
  --danger-color: #d32f2f; /* Vermelho */
  --warning-color: #ffa000; /* Amarelo */
  --info-color: #1976d2; /* Azul */
  --success-color: #388e3c; /* Verde */
  --border-radius: 0.5rem;
  --box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  --transition: all 0.3s ease-in-out;
}
```

### 2. Tipografia

**Localização**: `src/static/css/style.css`

**Descrição da Alteração**: A fonte padrão do corpo do documento foi alterada para 'Roboto', uma fonte moderna e legível, que melhora a estética geral da aplicação.

**Código Modificado (src/static/css/style.css)**:

```css
body {
  font-family: 'Roboto', sans-serif;
  color: var(--dark-text);
  background-color: var(--light-bg);
  line-height: 1.6;
}
```

### 3. Estilos de Componentes

Diversos componentes da interface foram aprimorados para refletir um design mais moderno e coeso:

#### Navbar

**Descrição**: A barra de navegação recebeu um fundo sólido com a `--primary-color` e uma sombra mais pronunciada para destacá-la. Os links de navegação agora têm um efeito de hover e estado ativo mais definidos, utilizando a `--secondary-color`.

**Código Modificado (src/static/css/style.css)**:

```css
.navbar {
  background: var(--primary-color) !important;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  padding: 1rem 1.5rem;
}

.navbar-brand {
  font-weight: 700;
  font-size: 1.5rem;
}

.navbar-dark .navbar-nav .nav-link {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  padding: 0.5rem 1rem;
  transition: var(--transition);
  border-radius: var(--border-radius);
  margin: 0 0.25rem;
}

.navbar-dark .navbar-nav .nav-link:hover, .navbar-dark .navbar-nav .nav-link.active {
  color: var(--light-text);
  background-color: var(--secondary-color);
}
```

#### Cards

**Descrição**: Os cards agora possuem bordas arredondadas maiores, sombras mais suaves e um efeito sutil de elevação (`translateY`) ao passar o mouse, conferindo uma sensação de profundidade e interatividade. O cabeçalho do card foi estilizado com a `--primary-color` e texto claro.

**Código Modificado (src/static/css/style.css)**:

```css
.card {
  border: none;
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  transition: var(--transition);
  margin-bottom: 2rem;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
}

.card-header {
  background-color: var(--primary-color);
  color: var(--light-text);
  border-bottom: none;
  padding: 1.25rem 1.5rem;
  font-weight: 500;
  border-top-left-radius: var(--border-radius);
  border-top-right-radius: var(--border-radius);
}

.card-body {
  padding: 2rem;
}
```

#### Botões

**Descrição**: Os botões foram redesenhados com cantos mais arredondados, texto em maiúsculas e um espaçamento de letras maior para um visual mais impactante. O botão primário (`.btn-primary`) agora utiliza a `--secondary-color` e tem um efeito de hover que muda para a `--accent-color` com uma leve elevação.

**Código Modificado (src/static/css/style.css)**:

```css
.btn {
  font-weight: 700;
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius);
  transition: var(--transition);
  text-transform: uppercase;
  letter-spacing: 1px;
  border: none;
}

.btn-primary {
  background-color: var(--secondary-color);
  color: var(--light-text);
}

.btn-primary:hover {
  background-color: var(--accent-color);
  color: var(--dark-text);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
```

#### Formulários

**Descrição**: Campos de formulário (`.form-control`, `.form-select`) receberam bordas mais definidas e um foco visual aprimorado com a `--secondary-color`. Os rótulos (`.form-label`) agora são mais proeminentes com `font-weight: 700`.

**Código Modificado (src/static/css/style.css)**:

```css
.form-control, .form-select {
  border: 2px solid #e0e0e0;
  border-radius: var(--border-radius);
  padding: 0.75rem 1rem;
  transition: var(--transition);
}

.form-control:focus, .form-select:focus {
  border-color: var(--secondary-color);
  box-shadow: 0 0 0 0.25rem rgba(92, 107, 192, 0.25);
}

.form-label {
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: var(--dark-text);
}
```

#### Tabelas

**Descrição**: As tabelas foram estilizadas para serem mais legíveis e visualmente atraentes. O cabeçalho da tabela agora tem um fundo com a `--primary-color` e texto em negrito. As linhas alternadas (`nth-child(even)`) e o efeito de hover (`:hover`) foram aprimorados para melhor diferenciação e interatividade.

**Código Modificado (src/static/css/style.css)**:

```css
.table {
  width: 100%;
  border-collapse: collapse;
}

.table thead th {
  background-color: var(--primary-color);
  color: var(--light-text);
  font-weight: 700;
  text-transform: uppercase;
  font-size: 0.9rem;
  letter-spacing: 0.5px;
  padding: 1rem;
  text-align: left;
}

.table tbody tr {
  border-bottom: 1px solid #e0e0e0;
}

.table tbody tr:nth-child(even) {
  background-color: #f9f9f9;
}

.table tbody tr:hover {
  background-color: rgba(92, 107, 192, 0.1);
}

.table td {
  padding: 1rem;
  vertical-align: middle;
}
```

#### Alertas

**Descrição**: Os alertas agora possuem uma borda lateral colorida que indica o tipo de mensagem (sucesso, perigo, aviso, informação), tornando-os mais distintos e informativos. O fundo e a cor do texto também foram ajustados para melhor contraste e legibilidade.

**Código Modificado (src/static/css/style.css)**:

```css
.alert {
  border-left: 5px solid;
  border-radius: var(--border-radius);
  padding: 1.25rem 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: var(--box-shadow);
}

.alert-success {
  border-color: var(--success-color);
  background-color: #e8f5e9;
  color: #1b5e20;
}

.alert-danger {
  border-color: var(--danger-color);
  background-color: #ffebee;
  color: #b71c1c;
}

.alert-warning {
  border-color: var(--warning-color);
  background-color: #fff8e1;
  color: #f57f17;
}

.alert-info {
  border-color: var(--info-color);
  background-color: #e3f2fd;
  color: #0d47a1;
}
```

#### Footer

**Descrição**: O rodapé foi simplificado com um fundo sólido usando a `--primary-color` e texto claro, garantindo consistência com a barra de navegação.

**Código Modificado (src/static/css/style.css)**:

```css
footer {
  background-color: var(--primary-color);
  color: var(--light-text);
  padding: 2rem 0;
  margin-top: 3rem;
}
```

## Conclusão

As alterações de CSS implementadas na branch `proj-002` visam modernizar a interface do usuário do AppTimeSheet, tornando-a mais atraente, intuitiva e profissional. O novo esquema de cores, tipografia e estilos de componentes contribuem para uma experiência visual aprimorada para o usuário.
