document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const dobInput = form.querySelector('input[name="date_of_birth"]');
    const parentContainer = document.getElementById('parentConsentContainer');
    const parentConsentInput = document.getElementById('parentConsentInput');

    form.addEventListener('submit', (e) => {
        e.preventDefault(); 

        const dobValue = dobInput.value;
        if (!dobValue) {
            alert('Пожалуйста, выберите дату рождения.');
            return;
        }

        const dob = new Date(dobValue);
        const today = new Date();

        let age = today.getFullYear() - dob.getFullYear();
        const monthDiff = today.getMonth() - dob.getMonth();
        const dayDiff = today.getDate() - dob.getDate();
        if (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0)) {
            age--;
        }

        const weekdays = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
        const dayOfWeek = weekdays[dob.getDay()];

        if (age >= 18) {
            alert(`Вы совершеннолетний (${age} лет). День недели вашей даты рождения: ${dayOfWeek}.`);
            form.submit(); 
        } else {
            alert(`Вы несовершеннолетний (${age} лет). Для использования сайта необходимо разрешение родителей.`);

            parentContainer.innerHTML = '';

            const consentDiv = document.createElement('div');
            consentDiv.innerHTML = `
                <p>Подтвердите согласие родителя на использование сайта:</p>
                <label>
                    <input type="checkbox" id="parentConsentCheckbox"> Я, родитель/опекун, даю согласие
                </label>
                <br><br>
                <button type="button" id="parentConsentButton">Подтвердить</button>
            `;
            parentContainer.appendChild(consentDiv);

            const consentButton = document.getElementById('parentConsentButton');
            const consentCheckbox = document.getElementById('parentConsentCheckbox');

            consentButton.addEventListener('click', (e) => {
                e.preventDefault();
                if (consentCheckbox.checked) {
                    parentConsentInput.value = 'true';
                    alert('Согласие получено. Регистрация завершена.');
                    form.submit(); 
                } else {
                    alert('Пожалуйста, отметьте согласие родителя.');
                }
            });
        }
    });
});
