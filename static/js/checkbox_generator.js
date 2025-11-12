document.addEventListener('DOMContentLoaded', () => {
    const trigger = document.getElementById('addCheckboxTrigger');
    const container = document.getElementById('checkboxContainer');
    const form = document.getElementById('checkboxForm');
    
    let checkboxes = JSON.parse(localStorage.getItem('checkboxes') || '[]');

    checkboxes.forEach(data => createCheckboxItem(data));

    trigger.addEventListener('change', () => {
        if (trigger.checked) {
            const newBoxData = {
                name: 'checkbox_' + Date.now(), // + текущее время в мс
                value: 'yes',
                checked: false,
                required: false,
                disabled: false
            };
            checkboxes.push(newBoxData);
            createCheckboxItem(newBoxData);
            saveToLocalStorage();
            trigger.checked = false; 
        }
    });

    function createCheckboxItem(data) {
        const wrapper = document.createElement('div');
        wrapper.className = 'checkbox-item';

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = data.name;
        checkbox.value = data.value;
        checkbox.checked = data.checked;
        checkbox.required = data.required;
        checkbox.disabled = data.disabled;

        const nameInput = createAttrInput('Имя (name):', data.name, val => {
            checkbox.name = val;
            data.name = val;
            saveToLocalStorage();
        });

        const valueInput = createAttrInput('Значение (value):', data.value, val => {
            checkbox.value = val;
            data.value = val;
            saveToLocalStorage();
        });

        const checkedInput = createAttrCheckbox('checked', data.checked, val => {
            checkbox.checked = val;
            data.checked = val;
            saveToLocalStorage();
        });

        const requiredInput = createAttrCheckbox('required', data.required, val => {
            checkbox.required = val;
            data.required = val;
            saveToLocalStorage();
        });

        const disabledInput = createAttrCheckbox('disabled', data.disabled, val => {
            checkbox.disabled = val;
            data.disabled = val;
            saveToLocalStorage();
        });

        const controls = document.createElement('div');
        controls.className = 'attr-controls';
        controls.append(nameInput, valueInput, checkedInput, requiredInput, disabledInput);

        const removeBtn = document.createElement('button');
        removeBtn.textContent = 'Удалить';
        removeBtn.type = 'button';
        removeBtn.className = 'remove-btn';
        removeBtn.addEventListener('click', () => {
            container.removeChild(wrapper);
            checkboxes = checkboxes.filter(c => c !== data);
            saveToLocalStorage();
        });

        wrapper.append(checkbox, controls, removeBtn);
        container.appendChild(wrapper);
    }

    function createAttrInput(labelText, value, onChange) {
        const label = document.createElement('label');
        label.textContent = labelText + ' ';
        const input = document.createElement('input');
        input.type = 'text';
        input.value = value;
        input.addEventListener('input', () => onChange(input.value));
        label.appendChild(input);
        return label;
    }

    function createAttrCheckbox(attr, value, onChange) {
        const label = document.createElement('label');
        label.textContent = attr + ': ';
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.checked = value;
        input.addEventListener('change', () => onChange(input.checked));
        label.appendChild(input);
        return label;
    }

    function saveToLocalStorage() {
        localStorage.setItem('checkboxes', JSON.stringify(checkboxes));
    }

    const submitBtn = document.getElementById('submitCheckboxesBtn');
    submitBtn.addEventListener('click', () => {
        const tempForm = document.createElement('form');

        container.querySelectorAll('input[type="checkbox"]').forEach(cb => {
            const clone = cb.cloneNode(true);
            tempForm.appendChild(clone);
        });

        if (tempForm.checkValidity()) {
            alert('Все обязательные чекбоксы выбраны — форма корректна!');
        } else {
            tempForm.reportValidity()
        }
    });
});
