document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme');

    if (currentTheme) {
        document.body.classList.add(currentTheme);
        updateButtonText(currentTheme);
    }

    toggleButton.addEventListener('click', () => {
        let theme;
        if (document.body.classList.contains('dark')) {
            document.body.classList.remove('dark');
            theme = 'light';
        } else {
            document.body.classList.add('dark');
            theme = 'dark';
        }

        localStorage.setItem('theme', theme);
        updateButtonText(theme);
    });

    function updateButtonText(theme) {
        toggleButton.textContent = theme === 'dark' ? '☀️ Светлая тема' : '🌙 Тёмная тема';
    }
});
