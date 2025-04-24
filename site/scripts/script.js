let API_URL = 'http://localhost:8000/api/v1';
let currentUser = null;
let cachedModels = null;
let authToken = localStorage.getItem('access_token');
const sendButton = document.getElementById('sendToGenerate');

const notificationToast = new bootstrap.Toast(document.getElementById('notificationToast'));

const MAX_IMAGES = 100;
const CACHE_KEY = 'user_images_cache';

// DOM элементы
const imageGrid = document.getElementById('imageGrid');


document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    loadModels();
    loadUserImages();
    
    setInterval(loadModels, 1 * 60 * 1000);
    
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
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error(await response.text());
        }

        const result = await response.json();
        showToastMessage(`Изображение "${formData.prompt}" создано!`);
        handleNewImage(result);
        
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

// Функция для загрузки изображений пользователя
async function loadUserImages() {
    try {
        // Проверяем кэш
        const cachedData = getCachedImages();
        if (cachedData && cachedData.length > 0) {
            renderImages(cachedData);
        }

        // Загружаем свежие данные
        const token = localStorage.getItem('access_token');
        if (!token) return;

        const response = await fetch(`${API_URL}/images`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) throw new Error('Ошибка загрузки изображений');

        const data = await response.json();
        
        // Сохраняем в кэш и рендерим
        cacheImages(data.images);
        renderImages(data.images);
        
    } catch (error) {
        console.error('Ошибка:', error);
        // Показываем кэшированные данные, если есть
        const cachedData = getCachedImages();
        if (cachedData && cachedData.length > 0) {
            renderImages(cachedData);
        }
    }
}

// Кэширование изображений
function cacheImages(images) {
    if (!images || !Array.isArray(images)) return;
    
    // Ограничиваем количество сохраняемых изображений
    const imagesToCache = images.slice(0, MAX_IMAGES);
    
    // Добавляем timestamp для контроля актуальности
    const cacheData = {
        timestamp: Date.now(),
        images: imagesToCache
    };
    
    localStorage.setItem(CACHE_KEY, JSON.stringify(cacheData));
}

// Получение кэшированных изображений
function getCachedImages() {
    const cache = localStorage.getItem(CACHE_KEY);
    if (!cache) return null;
    
    const cacheData = JSON.parse(cache);
    
    // Проверяем актуальность кэша (1 час)
    const isCacheValid = (Date.now() - cacheData.timestamp) < 3600000;
    
    return isCacheValid ? cacheData.images : null;
}

// Функция для обработки нового сгенерированного изображения
function handleNewImage(response) {
    console.log(response)
    if (response.status !== 'success') return;

    // Получаем текущие изображения из кэша
    const cachedData = getCachedImages() || [];
    
    // Добавляем новое изображение в начало
    const updatedImages = [
        {
            image_url: response.image.image_url,
            image_id: response.image.id
        },
        ...cachedData
    ].slice(0, MAX_IMAGES); // Сохраняем только MAX_IMAGES
    
    // Обновляем кэш и рендерим
    cacheImages(updatedImages);
    renderImages(updatedImages);
}

// Отображение изображений
function renderImages(images) {
    if (!images || !Array.isArray(images)) return;
    
    // Очищаем сетку
    imageGrid.innerHTML = '';
    
    // Ограничиваем количество отображаемых изображений
    const imagesToShow = images.slice(0, MAX_IMAGES);
    
    // Создаем карточки для каждого изображения
    imagesToShow.forEach(image => {
        const col = document.createElement('div');
        col.className = 'col';
        
        const card = document.createElement('div');
        card.className = 'card h-100';
        
        const img = document.createElement('img');
        img.className = 'card-img-top';
        img.src = image.image_url;
        img.alt = `Сгенерированное изображение ${image.image_id}`;
        img.loading = 'lazy'; // Ленивая загрузка
        
        const cardBody = document.createElement('div');
        cardBody.className = 'card-body';
        
        const downloadBtn = document.createElement('a');
        downloadBtn.className = 'btn btn-sm btn-outline-primary w-100';
        downloadBtn.href = image.image_url;
        downloadBtn.download = `ai_image_${image.image_id}.png`;
        downloadBtn.innerHTML = '<i class="fas fa-download me-2"></i>Скачать';
        
        cardBody.appendChild(downloadBtn);
        card.appendChild(img);
        card.appendChild(cardBody);
        col.appendChild(card);
        imageGrid.appendChild(col);
    });
}