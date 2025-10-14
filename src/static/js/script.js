// Script para funcionalidades interativas do sistema de Controle de Horas

document.addEventListener('DOMContentLoaded', function() {
    // Inicializa tooltips do Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Inicializa datepickers nos campos de data
    const datepickers = document.querySelectorAll('.datepicker');
    if (datepickers) {
        datepickers.forEach(function(element) {
            element.addEventListener('focus', function() {
                this.type = 'date';
            });
            element.addEventListener('blur', function() {
                if (!this.value) {
                    this.type = 'text';
                }
            });
        });
    }

    // Confirmação para exclusão
    const deleteButtons = document.querySelectorAll('.btn-delete');
    if (deleteButtons) {
        deleteButtons.forEach(function(button) {
            button.addEventListener('click', function(e) {
                if (!confirm('Tem certeza que deseja excluir este item?')) {
                    e.preventDefault();
                }
            });
        });
    }

    // Filtros dinâmicos para tabelas
    const filterInputs = document.querySelectorAll('.filter-input');
    if (filterInputs) {
        filterInputs.forEach(function(input) {
            input.addEventListener('keyup', function() {
                const tableId = this.getAttribute('data-table');
                const table = document.getElementById(tableId);
                if (table) {
                    filterTable(table, this.value, this.getAttribute('data-column'));
                }
            });
        });
    }

    // Função para filtrar tabelas
    function filterTable(table, value, columnIndex) {
        const rows = table.querySelectorAll('tbody tr');
        const filterValue = value.toLowerCase();
        
        rows.forEach(function(row) {
            const cell = row.querySelector(`td:nth-child(${parseInt(columnIndex) + 1})`);
            if (cell) {
                const text = cell.textContent.toLowerCase();
                if (text.indexOf(filterValue) > -1) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            }
        });
    }

    // Atualiza campos de formulário com base em seleções
    const dependentSelects = document.querySelectorAll('select[data-dependent]');
    if (dependentSelects) {
        dependentSelects.forEach(function(select) {
            select.addEventListener('change', function() {
                const targetId = this.getAttribute('data-dependent');
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    // Aqui você pode implementar lógica específica para atualizar o elemento alvo
                    // Por exemplo, fazer uma requisição AJAX para obter dados relacionados
                }
            });
        });
    }
});
