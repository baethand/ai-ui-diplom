let API_URL = 'http://localhost:8000/api/v1';
let currentUser = null;
let authToken = null;
let cachedModels = null;
const sendButton = document.getElementById('sendToGenerate');

const notificationToast = new bootstrap.Toast(document.getElementById('notificationToast'));
const generateForm = document.getElementById('generateForm');
const registerForm = document.getElementById('registerForm');


document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    loadModels();
    
    setInterval(loadModels, 5 * 60 * 1000);
    authToken = localStorage.getItem('authToken');
    // loadUserProfile();
});


generateForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (authToken == null){
        showToastMessage("Требуется аутентификация");
        return;
    }
    
    const spinner = document.getElementById('spinner');
    const submitText = document.getElementById('submitText');
    
    // Активируем состояние загрузки
    spinner.classList.remove('d-none');
    submitText.textContent = 'Генерация...';
    sendButton.disabled = true;
    
    try {
        // Собираем данные формы
        const formData = {
            prompt: document.getElementById('prompt').value,
            model: document.getElementById('model').value,
            num_inference_steps: parseInt(document.getElementById('numSteps').value),
            guidance_scale: parseFloat(document.getElementById('guidance').value),
            width: parseInt(document.getElementById('width').value),
            height: parseInt(document.getElementById('height').value)
        };

        // Отправляем запрос
        const response = await fetch(`${API_URL}/generate-image`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('authToken')}`
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error(await response.text());
        }

        const result = await response.json();
        showToastMessage(`Изображение "${formData.prompt}" создано!`);
        
    } catch (error) {
        console.error('Ошибка генерации:', error);
        showError('Ошибка при генерации изображения: ' + error.message);
    } finally {
        // Возвращаем кнопку в исходное состояние
        spinner.classList.add('d-none');
        submitText.textContent = 'Сгенерировать изображение';
        sendButton.disabled = false;
    }
});

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

    const themeSwitch = document.getElementById('themeSwitch');
    if (themeSwitch) {
        themeSwitch.addEventListener('change', function(e) {
            const isDark = e.target.checked;
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            document.documentElement.setAttribute('data-bs-theme', isDark ? 'dark' : 'light');
        });
    }

    async function loadModels() {
        const select = document.getElementById('model');
        
        select.innerHTML = '<option value="" disabled selected>Загрузка моделей...</option>';
        
        try {
            if (cachedModels) {
                updateModelSelect(cachedModels);
                return;
            }
    
            const response = await fetch(`${API_URL}/models`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (!data.models || !Array.isArray(data.models)) {
                throw new Error('Неверный формат данных моделей');
            }
            
            cachedModels = data.models;
            updateModelSelect(cachedModels);
            
        } catch (error) {
            console.error('Ошибка загрузки моделей:', error);
            select.innerHTML = '<option value="" disabled selected>Ошибка загрузки моделей</option>';
            showError('Не удалось загрузить модели');
        }
    }

    function updateModelSelect(models) {
        const select = document.getElementById('model');
        
        // Сохраняем выбранное значение (если было)
        const selectedValue = select.value;
        
        // Генерируем новые options
        select.innerHTML = `
            <option value="" disabled selected>Выберите модель</option>
            ${models.map(model => 
                `<option value="${model}">${model.split('/').pop()}</option>`
            ).join('')}
        `;
        
        // Восстанавливаем выбранное значение (если оно есть в новых моделях)
        if (selectedValue && models.includes(selectedValue)) {
            select.value = selectedValue;
        }
    }

    function showToastMessage(message) {
        document.getElementById('toastMessage').textContent = message;
        notificationToast.show();
    }

    

function showError(message) {
    const toast = document.getElementById('errorToast'); // Добавьте toast для ошибок в HTML
    toast.querySelector('.toast-body').textContent = message;
    new bootstrap.Toast(toast).show();
}

registerForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const username = document.getElementById('registerName').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    
    try {
        // Отправляем запрос на сервер
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Ошибка регистрации');
        }
        
        const data = await response.json();
        alert('Регистрация успешна!');
        console.log('Успешная регистрация:', data);
        localStorage.setItem('authToken', data.access_token);
        // Закрываем модальное окно после успешной регистрации
        const registerModal = bootstrap.Modal.getInstance(document.getElementById('registerModal'));
        registerModal.hide();
        
    } catch (error) {
        console.error('Ошибка регистрации:', error);
        alert(`Ошибка регистрации: ${error.message}`);
    }
});