function updateCardVisibility() {
    const cards = document.querySelectorAll('.recent-products .card');
    const isMax1200 = window.matchMedia("(max-width: 1200px)").matches;
    const isMax768 = window.matchMedia("(max-width: 768px)").matches;

    cards.forEach((card, index) => {
        if (isMax1200 && !isMax768 && index >= 9) {
            // Hide 10th card when between 769px and 1200px
            card.style.display = 'none';
        } else {
            // Show all cards on >1200px or ≤768px
            card.style.display = '';
        }
    });
}

window.addEventListener('load', updateCardVisibility);
window.addEventListener('resize', updateCardVisibility);