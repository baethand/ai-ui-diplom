let API_URL = 'http://localhost:8000/api/v1';

document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    console.log('Login form exists:', document.getElementById('loginForm') !== null);
    console.log('Register form exists:', document.getElementById('registerForm') !== null);

    // Авторизация
    if (loginForm) {
        loginForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const email = document.getElementById('loginOrEmail').value;
            const password = document.getElementById('loginPassword').value;

            const data = {
                usernameOrEmail: email,
                password: password
            };


            try {
                const response = await fetch(`${API_URL}/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                

                const result = await response.json();
                if (!response.ok) {
                    alert('Ошибка входа: ' + result.detail);
                    return;
                }

                localStorage.setItem('access_token', result.access_token);
                localStorage.setItem('refresh_token', result.refresh_token);
                localStorage.setItem('email', email);  // сохраняем email

                window.location.href = '/site/pages/generator.html';
            } catch (error) {
                console.error('Ошибка при входе:', error);
            }
        });
    }

    // Регистрация
    if (registerForm) {
        registerForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const name = document.getElementById('registerName').value;
            const email = document.getElementById('registerEmail').value;
            const password = document.getElementById('registerPassword').value;

            const data = {
                username: name,
                email: email,
                password: password
            };

            try {
                const response = await fetch(`${API_URL}/register`, {  // Fixed: added API_URL
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                if (!response.ok) {
                    alert('Ошибка регистрации: ' + result.detail);
                    return;
                }

                localStorage.setItem('access_token', result.access_token);
                localStorage.setItem('refresh_token', result.refresh_token);

                window.location.href = '/site/pages/generator.html';
            } catch (error) {
                console.error('Ошибка при регистрации:', error);
            }
        });
    }
});

