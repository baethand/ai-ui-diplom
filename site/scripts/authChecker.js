document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');

    // 1. Если токена нет — сразу редирект
    if (!token) {
        redirectToLogin();
        return;
    }

    // 2. Парсим токен и проверяем его срок
    try {
        const jwtPayload = parseJwt(token);
        console.log("JWT Payload:", jwtPayload);

        // 3. Проверяем expiration time (exp)
        if (isTokenExpired(jwtPayload.exp)) {
            alert('Сессия истекла. Пожалуйста, войдите снова.');
            console.error("Токен просрочен!");
            clearAuthData();
            redirectToLogin();
            return;
        }

        // 4. Если токен валиден — показываем контент
        const usernameElement = document.getElementById('user-username');
        if (usernameElement) {
            usernameElement.textContent = jwtPayload.sub;
        } else {
            console.warn('Элемент #user-username не найден!');
        }
        console.log("Токен действителен. Пользователь:", jwtPayload.sub);

        // кнопка выхода
        const logoutBtn = document.getElementById('logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', handleLogout);
        } else {
            console.warn('Кнопка выхода не найдена!');
        }
        
    } catch (e) {
        console.error("Ошибка при проверке токена:", e);
        clearAuthData();
        redirectToLogin();
    }
});

function handleLogout() {
    clearAuthData();
    redirectToLogin();
}

// Проверяет, истек ли срок действия токена
function isTokenExpired(expTimestamp) {
    if (!expTimestamp) return true; // Если нет exp — считаем просроченным
    
    const currentTime = Math.floor(Date.now() / 1000); // Текущее время в секундах
    return expTimestamp < currentTime;
}

// Очищает данные авторизации
function clearAuthData() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('email');
}

// Перенаправляет на страницу входа
function redirectToLogin() {
    window.location.href = '/site/pages/index.html';
}

function parseJwt(token) {
    try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(
            window.atob(base64)
                .split('')
                .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
                .join('')
        );
        return JSON.parse(jsonPayload);
    } catch (e) {
        console.error("Ошибка при парсинге JWT:", e);
        return null;
    }
}