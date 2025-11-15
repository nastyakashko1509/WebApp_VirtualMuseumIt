document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.querySelector('#employeesTable tbody');
    const preloader = document.getElementById('preloader');
    const filterInput = document.getElementById('searchInput');
    const filterBtn = document.getElementById('filterBtn');
    const awardBtn = document.getElementById('awardBtn');
    const awardResult = document.getElementById('awardResult');
    const selectedDetails = document.getElementById('selectedDetails');

    const addEmployeeBtn = document.getElementById('addEmployeeBtn');
    const addEmployeeFormWrapper = document.getElementById('addEmployeeFormWrapper');
    const addEmployeeForm = document.getElementById('addEmployeeForm');
    const submitEmployeeBtn = document.getElementById('submitEmployeeBtn');
    const validationResult = document.getElementById('validationResult');

    const empFullName = document.getElementById('empFullName');
    const empPhotoUrl = document.getElementById('empPhotoUrl');
    const empWorkDesc = document.getElementById('empWorkDesc');
    const empPhone = document.getElementById('empPhone');
    const empEmail = document.getElementById('empEmail');

    let employees = [];
    let sortField = '';
    let sortAsc = true;

    const rowsPerPage = 3;
    let currentPage = 1;
    const paginationContainer = document.createElement('div');
    paginationContainer.id = 'pagination';
    paginationContainer.style.marginBottom = '20px';
    paginationContainer.style.whiteSpace = 'nowrap'; // отмена переноса
    tableBody.parentNode.insertBefore(paginationContainer, tableBody.nextSibling);

    preloader.style.display = 'block';
    setTimeout(() => {
        fetch('/api/employees/')
            .then(res => res.json())
            .then(data => {
                employees = data.map(emp => ({...emp, selected: false})); // добавляем поле selected
                preloader.style.display = 'none';
                renderTable(employees);
                renderPagination(employees);
            });
    }, 3000);

    function td(key, value) {
        const tdEl = document.createElement('td');
        tdEl.textContent = value;
        return tdEl;
    }

    function renderTable(data) {
        tableBody.innerHTML = '';
        const start = (currentPage - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        const pageData = data.slice(start, end);

        pageData.forEach((emp, index) => {
            const tr = document.createElement('tr');
            tr.classList.add('employee-row');

            const tdCheck = document.createElement('td');
            const cb = document.createElement('input');
            cb.type = 'checkbox';
            cb.checked = emp.selected || false;
            cb.addEventListener('change', () => {
                employees[start + index].selected = cb.checked; // сохранение состояний
            });
            tdCheck.appendChild(cb);
            tr.appendChild(tdCheck);

            tr.appendChild(td('full_name', emp.full_name));
            tr.appendChild(td('age', emp.age));
            tr.appendChild(td('position', emp.position));
            tr.appendChild(td('phone', emp.phone));
            tr.appendChild(td('email', emp.email));
            tr.appendChild(td('bio', emp.bio || emp.work_description || ''));

            tr.addEventListener('click', (e) => {
                if (e.target.type !== 'checkbox') {
                    selectedDetails.innerHTML = `<p>Выбрано: ${emp.full_name}, возраст: ${emp.age}, должность: ${emp.position}</p>`;
                }
            });

            tableBody.appendChild(tr);
        });
    }

    function renderPagination(data) {
        paginationContainer.innerHTML = '';
        const pageCount = Math.ceil(data.length / rowsPerPage);
        for (let i = 1; i <= pageCount; i++) {
            const btn = document.createElement('button');
            btn.textContent = i;
            btn.style.margin = '0 5px';
            btn.disabled = i === currentPage;
            btn.addEventListener('click', () => {
                currentPage = i;
                renderTable(employees);
                renderPagination(employees);
            });
            paginationContainer.appendChild(btn);
        }
    }

    document.querySelectorAll('#employeesTable th[data-sort]').forEach(th => {
        th.addEventListener('click', () => {
            const field = th.dataset.sort;
            sortAsc = (sortField === field) ? !sortAsc : true; // изменение направления
            sortField = field;

            employees.sort((a,b) => {
                if(a[field] < b[field]) return sortAsc ? -1 : 1;
                if(a[field] > b[field]) return sortAsc ? 1 : -1;
                return 0;
            });

            document.querySelectorAll('#employeesTable th').forEach(thEl => thEl.classList.remove('sorted-asc', 'sorted-desc'));
            th.classList.add(sortAsc ? 'sorted-asc' : 'sorted-desc');

            renderTable(employees);
            renderPagination(employees);
        });
    });

    filterBtn.addEventListener('click', () => {
        const term = filterInput.value.toLowerCase();
        const filtered = employees.filter(emp => 
            emp.full_name.toLowerCase().includes(term) || (emp.position && emp.position.toLowerCase().includes(term))
        );
        currentPage = 1;
        renderTable(filtered);
        renderPagination(filtered);
    });

    awardBtn.addEventListener('click', () => {
        const awarded = employees.filter(emp => emp.selected).map(emp => emp.full_name);
        awardResult.textContent = awarded.length ? `Премируются: ${awarded.join(', ')}` : 'Не выбрано ни одного сотрудника.';
    });

    // показ/скрытие формы добавления
    addEmployeeBtn.addEventListener('click', () => {
        addEmployeeFormWrapper.style.display = addEmployeeFormWrapper.style.display === 'none' ? 'block' : 'none';
    });

    function validateURL(url) {
        return /^(https?:\/\/).*(\.php|\.html)$/.test(url);
    }

    function validatePhone(phone) {
        const patterns = [
            /^8029\d{7}$/,
            /^8 ?\((25|29|33|44)\) ?\d{7}$/,
            /^\+375 ?\((25|29|33|44)\) ?\d{3}-?\d{2}-?\d{2}$/
        ];
        return patterns.some(p => p.test(phone.replace(/\s+/g,'')));
    }

    function checkAllFieldsFilled() {
        return empFullName.value.trim() !== '' &&
               empPhotoUrl.value.trim() !== '' &&
               empWorkDesc.value.trim() !== '' &&
               empPhone.value.trim() !== '' &&
               empEmail.value.trim() !== '';
    }

    function updateSubmitButtonState() {
        submitEmployeeBtn.disabled = !checkAllFieldsFilled();
    }

    [empFullName, empPhotoUrl, empWorkDesc, empPhone, empEmail].forEach(input => {
        input.addEventListener('input', updateSubmitButtonState);
    });

    updateSubmitButtonState(); 

    submitEmployeeBtn.addEventListener('click', () => {
        let valid = true;
        validationResult.textContent = '';
        [empPhotoUrl, empPhone].forEach(el => el.classList.remove('invalid'));

        if(!validateURL(empPhotoUrl.value)) {
            empPhotoUrl.classList.add('invalid');
            validationResult.textContent += 'Неверный URL. ';
            valid = false;
        }

        if(!validatePhone(empPhone.value)) {
            empPhone.classList.add('invalid');
            validationResult.textContent += 'Неверный номер телефона. ';
            valid = false;
        }

        if(!valid) return;

        const newEmployee = {
            full_name: empFullName.value,
            photo: empPhotoUrl.value,
            work_description: empWorkDesc.value,
            phone: empPhone.value,
            email: empEmail.value,
            age: '—',
            position: '—',
            bio: empWorkDesc.value,
            selected: false
        };

        employees.push(newEmployee);
        currentPage = Math.ceil(employees.length / rowsPerPage);
        renderTable(employees);
        renderPagination(employees);

        addEmployeeForm.reset();
        validationResult.textContent = 'Сотрудник добавлен!';
        updateSubmitButtonState();
    });
});
