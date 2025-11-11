document.addEventListener('DOMContentLoaded', () => {
    const setup = document.getElementById('setup').innerText;
    const punchline = document.getElementById('punchline').innerText;
    const speakButton = document.getElementById('speakJoke');
    const batteryInfo = document.getElementById('batteryInfo');

    if ('speechSynthesis' in window) {
        speakButton.addEventListener('click', () => {
            const utterance = new SpeechSynthesisUtterance(`${setup}. ${punchline}`);
            utterance.lang = 'en-US';
            utterance.rate = 1; // скорость речи
            utterance.pitch = 1; // высота речи
            window.speechSynthesis.speak(utterance);
        });
    } else {
        speakButton.style.display = 'none';
        const warning = document.createElement('p');
        warning.textContent = 'Синтез речи не поддерживается вашим браузером.';
        document.body.appendChild(warning);
    }

    if ('getBattery' in navigator) {
        navigator.getBattery().then(battery => {
            function updateBatteryInfo() {
                const level = Math.round(battery.level * 100);
                const charging = battery.charging ? 'заряжается' : 'не заряжается';
                batteryInfo.textContent = `Уровень заряда: ${level}%. Сейчас ${charging}.`;
            }

            updateBatteryInfo();

            battery.addEventListener('levelchange', updateBatteryInfo);
            battery.addEventListener('chargingchange', updateBatteryInfo);
        });
    } else {
        batteryInfo.textContent = 'Ваш браузер не поддерживает Battery API.';
    }
});
