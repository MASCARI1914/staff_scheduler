// static/js/login.js
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('form');

    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            const emailInput = loginForm.querySelector('input[type="text"]'); // Αν το email είναι στο username field
            // ή:
            // const emailInput = loginForm.querySelector('input[type="email"]'); // Αν έχετε ξεχωριστό πεδίο email

            if (emailInput && !emailInput.value.endsWith('@gmail.com')) {
                e.preventDefault(); // Ακύρωση υποβολής
                alert('Το email πρέπει να τελειώνει με @gmail.com');
            }
        });
    }
});

fetch('/check_email', {
    method: 'POST',
    body: JSON.stringify({ email: emailInput.value }),
    headers: { 'Content-Type': 'application/json' }
})
.then(response => response.json())
.then(data => {
    if (data.exists) {
        alert('Το email χρησιμοποιείται ήδη!');
    }
});