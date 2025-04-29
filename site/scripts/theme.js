export function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'system';
    const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.setAttribute('data-bs-theme',
        (savedTheme === 'dark' || (savedTheme === 'system' && systemDark)) ? 'dark' : 'light');
    const switchEl = document.getElementById('themeSwitch');
    if (switchEl) {
        switchEl.checked = savedTheme === 'dark';
        switchEl.addEventListener('change', (e) => {
            const isDark = e.target.checked;
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            document.documentElement.setAttribute('data-bs-theme', isDark ? 'dark' : 'light');
        });
    }
}
