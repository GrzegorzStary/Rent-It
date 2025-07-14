function updateCardVisibility() {
    const cards = document.querySelectorAll('.recent-products .card');
    const screenWidth = window.innerWidth;
    let maxVisible = cards.length; 

    if (screenWidth >= 1440) {
        maxVisible = 8;
    } else if (screenWidth >= 1024) {
        maxVisible = 6; 
    } else if (screenWidth >= 768) {
        maxVisible = 8; 
    }

    cards.forEach((card, index) => {
        card.style.display = index < maxVisible ? '' : 'none';
    });
}

window.addEventListener('load', updateCardVisibility);
window.addEventListener('resize', updateCardVisibility);
