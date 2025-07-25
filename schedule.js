document.addEventListener('DOMContentLoaded', () => {
    const shiftForm = document.getElementById('shiftForm');
    const errorMessage = document.getElementById('error-message');

    if (shiftForm) {
        shiftForm.addEventListener('submit', (e) => {
            errorMessage.textContent = '';
            
            const userSelect = shiftForm.querySelector('select[name="user_id"]');
            const dateInput = shiftForm.querySelector('input[name="date"]');
            const startInput = shiftForm.querySelector('input[name="start"]');
            const endInput = shiftForm.querySelector('input[name="end"]');
            
            // Βασικοί έλεγχοι
            if (!userSelect.value || !dateInput.value || !startInput.value || !endInput.value) {
                e.preventDefault();
                errorMessage.textContent = 'Συμπληρώστε όλα τα πεδία';
                return;
            }
            
            // Έλεγχος ώρας
            const [startH, startM] = startInput.value.split(':').map(Number);
            const [endH, endM] = endInput.value.split(':').map(Number);
            
            // Υπολογισμός διάρκειας (με υποστήριξη νυχτερινών βαρδιών)
            let totalMinutes;
            if (endH < startH || (endH == startH && endM < startM)) {
                // Νυχτερινή βάρδια
                totalMinutes = (24 * 60 - (startH * 60 + startM)) + (endH * 60 + endM);
            } else {
                // Κανονική βάρδια
                totalMinutes = (endH * 60 + endM) - (startH * 60 + startM);
            }
            
            if (totalMinutes <= 0) {
                e.preventDefault();
                errorMessage.textContent = 'Η ώρα λήξης πρέπει να είναι μετά την ώρα έναρξης';
                return;
            }
            
            if (totalMinutes < 60) {
                e.preventDefault();
                errorMessage.textContent = 'Η βάρδια πρέπει να είναι τουλάχιστον 1 ώρα';
                return;
            }
        });
    }

    // Χειρισμός διαγραφής μέσω fetch
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Είστε σίγουρος ότι θέλετε να διαγράψετε αυτή τη βάρδια;')) {
                e.preventDefault();
            }
        });
    });
});