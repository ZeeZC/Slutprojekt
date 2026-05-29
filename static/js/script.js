//JavaScript för telefonboken

//Auto-hide alerts efter 5 sekunder
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                if (alert.parentElement) {
                    alert.style.display = 'none';
                }
            }, 300);
        }, 5000);
    });
});

//Live-sökning på index-sidan
function searchContacts() {
    const input = document.getElementById('searchInput');
    if (!input) return;
    
    const filter = input.value.toLowerCase();
    const cards = document.getElementsByClassName('contact-card');
    
    for (let card of cards) {
        const name = card.getAttribute('data-name');
        if (name && name.includes(filter)) {
            card.style.display = '';
        } else if (card.style) {
            card.style.display = 'none';
        }
    }
}

//Bekräfta borttagning
function confirmDelete(contactName) {
    return confirm(`Är du säker på att du vill ta bort ${contactName}?`);
}