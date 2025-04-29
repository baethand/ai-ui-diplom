import { initTheme } from './theme.js';
import { loadModels } from './models.js';
import { loadUserImages, handleNewImage } from './images.js';
import { showToastMessage, showError } from './notifications.js';

const API_URL = 'http://localhost:8000/api/v1';
const authToken = localStorage.getItem('access_token');
const sendButton = document.getElementById('sendToGenerate');

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    loadModels(API_URL).then(restoreFormState);
    loadUserImages(API_URL, authToken);
    setInterval(() => loadModels(API_URL), 60000);
});

document.getElementById('generateForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!authToken) {
        showToastMessage("Требуется аутентификация");
        return;
    }

    const spinner = document.getElementById('spinner');
    const submitText = document.getElementById('submitText');
    spinner.classList.remove('d-none');
    submitText.textContent = 'Генерация...';
    sendButton.disabled = true;

    try {
        const data = {
            prompt: document.getElementById('prompt').value,
            model_path: document.getElementById('model').value,
            num_inference_steps: +document.getElementById('numSteps').value,
            guidance_scale: +document.getElementById('guidance').value,
            width: +document.getElementById('width').value,
            height: +document.getElementById('height').value
        };

        const res = await fetch(`${API_URL}/generate-image`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(data)
        });

        if (!res.ok) throw new Error(await res.text());

        const result = await res.json();
        showToastMessage(`Изображение "${data.prompt}" создано!`);
        handleNewImage(result);

    } catch (err) {
        showError('Ошибка генерации изображения: ' + err.message);
    } finally {
        spinner.classList.add('d-none');
        submitText.textContent = 'Сгенерировать изображение';
        sendButton.disabled = false;
    }
});

function restoreFormState() {
    const state = JSON.parse(localStorage.getItem('formState'));
    if (!state) return;

    document.getElementById('prompt').value = state.prompt || '';
    document.getElementById('numSteps').value = state.numSteps || 20;
    document.getElementById('guidance').value = state.guidance || 7.5;
    document.getElementById('width').value = state.width || 512;
    document.getElementById('height').value = state.height || 512;

    const modelSelect = document.getElementById('model');
    const restoreModel = () => {
        if ([...modelSelect.options].some(opt => opt.value === state.model)) {
            modelSelect.value = state.model;
        }
    };

    if (modelSelect.options.length > 1) {
        restoreModel();
    } else {
        const observer = new MutationObserver(() => {
            restoreModel();
            observer.disconnect();
        });
        observer.observe(modelSelect, { childList: true });
    }
}


function saveFormState() {
    const state = {
        prompt: document.getElementById('prompt').value,
        model: document.getElementById('model').value,
        numSteps: document.getElementById('numSteps').value,
        guidance: document.getElementById('guidance').value,
        width: document.getElementById('width').value,
        height: document.getElementById('height').value
    };
    localStorage.setItem('formState', JSON.stringify(state));
}

document.getElementById('generateForm').addEventListener('input', saveFormState);
