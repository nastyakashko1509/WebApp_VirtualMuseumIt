document.addEventListener('DOMContentLoaded', () => {
    const employeesContainer = document.querySelector('.employees-container');
    const employeeCards = Array.from(employeesContainer.querySelectorAll('.employee-card'));
    
    const paginationContainer = document.createElement('div');
    paginationContainer.className = 'pagination-container';
    employeesContainer.parentNode.insertBefore(paginationContainer, employeesContainer.nextSibling);

    let currentPage = 1;
    let itemsPerPage = 3; 
    const itemsPerPageSelect = document.createElement('select');

    [3, 5, 10].forEach(num => {
        const option = document.createElement('option');
        option.value = num;
        option.textContent = `${num} на страницу`;
        if (num === itemsPerPage) option.selected = true;
        itemsPerPageSelect.appendChild(option);
    });

    paginationContainer.appendChild(itemsPerPageSelect);

    const pagesNav = document.createElement('div');
    pagesNav.className = 'pages-nav';
    paginationContainer.appendChild(pagesNav);

    function renderPage(page) {
        const start = (page - 1) * itemsPerPage;
        const end = start + itemsPerPage;

        employeeCards.forEach((card, index) => {
            if (index >= start && index < end) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });

        renderPagination();
    }

    function renderPagination() {
        const totalPages = Math.ceil(employeeCards.length / itemsPerPage);
        pagesNav.innerHTML = '';

        for (let i = 1; i <= totalPages; i++) {
            const pageBtn = document.createElement('button');
            pageBtn.textContent = i;
            pageBtn.className = i === currentPage ? 'active-page' : '';
            pageBtn.addEventListener('click', () => {
                currentPage = i;
                renderPage(currentPage);
            });
            pagesNav.appendChild(pageBtn);
        }
    }

    itemsPerPageSelect.addEventListener('change', () => {
        itemsPerPage = parseInt(itemsPerPageSelect.value);
        currentPage = 1;
        renderPage(currentPage);
    });

    renderPage(currentPage);
});
