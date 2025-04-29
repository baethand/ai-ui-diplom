const MAX_IMAGES = 100;
const CACHE_KEY = 'user_images_cache';

export function getCachedImages() {
    const cache = JSON.parse(localStorage.getItem(CACHE_KEY));
    const isValid = cache && (Date.now() - cache.timestamp < 3600000);
    return isValid ? cache.images : null;
}

export function cacheImages(images) {
    localStorage.setItem(CACHE_KEY, JSON.stringify({
        timestamp: Date.now(),
        images: images.slice(0, MAX_IMAGES)
    }));
}

export function renderImages(images) {
    const container = document.getElementById('imageGrid');
    container.innerHTML = '';
    images.slice(0, MAX_IMAGES).forEach(({ image_url, image_id }) => {
        const col = document.createElement('div');
        col.className = 'col';
        col.innerHTML = `
            <div class="card h-100">
                <img src="${image_url}" class="card-img-top" alt="Сгенерированное изображение ${image_id}" loading="lazy">
                <div class="card-body">
                    <a class="btn btn-sm btn-outline-primary w-100" href="${image_url}" download="ai_image_${image_id}.png">
                        <i class="fas fa-download me-2"></i>Скачать
                    </a>
                </div>
            </div>
        `;
        container.appendChild(col);
    });
}

export async function loadUserImages(apiUrl, token) {
    const cached = getCachedImages();
    if (cached) renderImages(cached);

    try {
        const res = await fetch(`${apiUrl}/images`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        const data = await res.json();
        cacheImages(data.images);
        renderImages(data.images);
    } catch (e) {
        console.error(e);
        if (cached) renderImages(cached);
    }
}

export function handleNewImage(response) {
    if (response.status !== 'success') return;
    const cached = getCachedImages() || [];
    const updated = [{ image_url: response.image.image_url, image_id: response.image.id }, ...cached];
    cacheImages(updated);
    renderImages(updated);
}
