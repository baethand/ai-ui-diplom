// Исправляем ошибку 'generateForm' null
document.addEventListener('DOMContentLoaded', () => {
    // 1. Переносим инициализацию элементов в DOMContentLoaded
    const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
    const registerModal = new bootstrap.Modal(document.getElementById('registerModal'));
    const notificationToast = new bootstrap.Toast(document.getElementById('notificationToast'));

    // 2. Проверяем существование формы
    const generateForm = document.getElementById('generateForm');
    if (!generateForm) {
        console.error('Форма генерации не найдена! Проверьте ID элемента');
        return;
    }

    // 3. Обработчик для формы
    generateForm.addEventListener('submit', async (e) => {
        // ... ваш существующий код обработки ... 
    });

    // 4. Убираем дублирование initTheme()
    function initTheme() {
        const savedTheme = localStorage.getItem('theme') || 'system';
        const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        document.documentElement.setAttribute('data-bs-theme', 
            (savedTheme === 'dark' || (savedTheme === 'system' && systemDark)) 
                ? 'dark' 
                : 'light'
        );
        document.getElementById('themeSwitch').checked = (savedTheme === 'dark');
    }

    // 5. Вешаем обработчик на переключатель
    const themeSwitch = document.getElementById('themeSwitch');
    if (themeSwitch) {
        themeSwitch.addEventListener('change', function(e) {
            const isDark = e.target.checked;
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            document.documentElement.setAttribute('data-bs-theme', isDark ? 'dark' : 'light');
        });
    }

    // 6. Добавляем недостающие функции
    function showError(message) {
        const toast = document.getElementById('errorToast'); // Добавьте toast для ошибок в HTML
        toast.querySelector('.toast-body').textContent = message;
        new bootstrap.Toast(toast).show();
    }

    function showSuccess(message) {
        document.getElementById('toastMessage').textContent = message;
        notificationToast.show();
    }

    // 7. Инициализация
    initTheme();
    loadModels();
    authToken = localStorage.getItem('authToken');
    // loadUserProfile(); // Раскомментируйте после реализации
});