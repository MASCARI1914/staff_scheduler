// static/js/register.js
document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.querySelector('form');

    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            const emailInput = registerForm.querySelector('input[type="email"]');

            if (emailInput && !emailInput.value.endsWith('@gmail.com')) {
                e.preventDefault();
                alert('Μόνο emails @gmail.com επιτρέπονται!');
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


   // Επιβεβαίωση πριν την υποβολή
    form.addEventListener('submit', (e) => {
        if (errorDiv.textContent !== '') {
            e.preventDefault();
            alert('Διόρθωσε τα σφάλματα πριν την υποβολή!');
        }
    });
