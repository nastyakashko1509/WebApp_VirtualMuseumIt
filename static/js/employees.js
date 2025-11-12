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

    // Показать преоладер и имитация задержки загрузки
    preloader.style.display = 'block';
    setTimeout(() => {
        fetch('/api/employees/')
            .then(res => res.json())
            .then(data => {
                employees = data;
                preloader.style.display = 'none';
                renderTable(employees);
            });
    }, 3000); // 3 секунды задержки

    function renderTable(data) {
        tableBody.innerHTML = '';
        data.forEach((emp, index) => {
            const tr = document.createElement('tr');
            tr.classList.add('employee-row');

            const tdCheck = document.createElement('td');
            const cb = document.createElement('input');
            cb.type = 'checkbox';
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

    function td(key, value) {
        const tdEl = document.createElement('td');
        tdEl.textContent = value;
        return tdEl;
    }

    // Сортировка по столбцам
    document.querySelectorAll('#employeesTable th[data-sort]').forEach(th => {
        th.addEventListener('click', () => {
            const field = th.dataset.sort;
            sortAsc = (sortField === field) ? !sortAsc : true;
            sortField = field;

            employees.sort((a,b) => {
                if(a[field] < b[field]) return sortAsc ? -1 : 1;
                if(a[field] > b[field]) return sortAsc ? 1 : -1;
                return 0;
            });

            document.querySelectorAll('#employeesTable th').forEach(thEl => thEl.classList.remove('sorted-asc', 'sorted-desc'));
            th.classList.add(sortAsc ? 'sorted-asc' : 'sorted-desc');

            renderTable(employees);
        });
    });

    // Фильтр
    filterBtn.addEventListener('click', () => {
        const term = filterInput.value.toLowerCase();
        const filtered = employees.filter(emp => 
            emp.full_name.toLowerCase().includes(term) || (emp.position && emp.position.toLowerCase().includes(term))
        );
        renderTable(filtered);
    });

    // Премирование выбранных
    awardBtn.addEventListener('click', () => {
        const awarded = [];
        tableBody.querySelectorAll('tr').forEach((tr, idx) => {
            const cb = tr.querySelector('input[type="checkbox"]');
            if(cb.checked) awarded.push(employees[idx].full_name);
        });
        awardResult.textContent = awarded.length ? `Премируются: ${awarded.join(', ')}` : 'Не выбрано ни одного сотрудника.';
    });

    // Показ/скрытие формы добавления сотрудника
    addEmployeeBtn.addEventListener('click', () => {
        addEmployeeFormWrapper.style.display = addEmployeeFormWrapper.style.display === 'none' ? 'block' : 'none';
    });

    // Валидация URL
    function validateURL(url) {
        return /^(https?:\/\/).*(\.php|\.html)$/.test(url);
    }

    // Валидация телефона
    function validatePhone(phone) {
        const patterns = [
            /^8029\d{7}$/,
            /^8 ?\((25|29|33|44)\) ?\d{7}$/,
            /^\+375 ?\((25|29|33|44)\) ?\d{3}-?\d{2}-?\d{2}$/
        ];
        return patterns.some(p => p.test(phone.replace(/\s+/g,'')));
    }

    // Проверка всех полей на заполненность
    function checkAllFieldsFilled() {
        return empFullName.value.trim() !== '' &&
               empPhotoUrl.value.trim() !== '' &&
               empWorkDesc.value.trim() !== '' &&
               empPhone.value.trim() !== '' &&
               empEmail.value.trim() !== '';
    }

    // Включение/отключение кнопки добавления
    function updateSubmitButtonState() {
        submitEmployeeBtn.disabled = !checkAllFieldsFilled();
    }

    [empFullName, empPhotoUrl, empWorkDesc, empPhone, empEmail].forEach(input => {
        input.addEventListener('input', updateSubmitButtonState);
    });

    updateSubmitButtonState(); // инициализация состояния кнопки

    // Добавление сотрудника
    submitEmployeeBtn.addEventListener('click', () => {
        let valid = true;
        validationResult.textContent = '';

        // Сброс визуальных ошибок
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
            bio: empWorkDesc.value
        };

        employees.push(newEmployee);
        renderTable(employees);

        // Очистка формы
        addEmployeeForm.reset();
        validationResult.textContent = 'Сотрудник добавлен!';
        updateSubmitButtonState(); // отключаем кнопку после добавления
    });
});
