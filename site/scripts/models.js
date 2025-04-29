let cachedModels = null;
const MODELS_CACHE_KEY = 'models_cache';
// const MODELS_CACHE_TTL = 3600000; // 1 час = 3600000 мс
const MODELS_CACHE_TTL = 10; // 1 час = 3600000 мс

export async function loadModels(apiUrl) {
    const select = document.getElementById('model');
    select.innerHTML = '<option disabled selected>Загрузка моделей...</option>';

    try {
        // Проверка кэша в памяти
        if (cachedModels) {
            updateModelSelect(cachedModels);
            return;
        }

        // Проверка кэша в localStorage
        const cached = localStorage.getItem(MODELS_CACHE_KEY);
        if (cached) {
            const { timestamp, models } = JSON.parse(cached);
            const isCacheValid = (Date.now() - timestamp) < MODELS_CACHE_TTL;

            if (isCacheValid && Array.isArray(models)) {
                cachedModels = models;
                updateModelSelect(models);
                return;
            }
        }

        // Запрос с сервера
        const res = await fetch(`${apiUrl}/models`);
        const { models } = await res.json();
        if (!models || !Array.isArray(models)) throw new Error('Неверный формат');

        cachedModels = models;
        updateModelSelect(models);

        // Сохраняем в localStorage
        localStorage.setItem(MODELS_CACHE_KEY, JSON.stringify({
            timestamp: Date.now(),
            models
        }));

    } catch (e) {
        console.error('Ошибка загрузки моделей:', e);
        select.innerHTML = '<option disabled selected>Ошибка загрузки</option>';
    }
}

function updateModelSelect(models) {
    const select = document.getElementById('model');
    const prevValue = select.value;

    select.innerHTML = `
        <option disabled selected>Выберите модель</option>
        ${models.map(m => `<option value="${m}">${m.split('/').pop()}</option>`).join('')}
    `;

    if (models.includes(prevValue)) select.value = prevValue;
}
