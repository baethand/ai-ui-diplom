export function showToastMessage(msg) {
    document.getElementById('toastMessage').textContent = msg;
    new bootstrap.Toast(document.getElementById('notificationToast')).show();
}

export function showError(msg) {
    const toast = document.getElementById('errorToast');
    toast.querySelector('.toast-body').textContent = msg;
    new bootstrap.Toast(toast).show();
}
