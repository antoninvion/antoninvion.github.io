const slide = document.querySelector('.carousel-slide');
const items = document.querySelectorAll('.carousel-item');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

let counter = 0;
const size = items[0].clientWidth + 20; // largeur + marge

function updateSlidePosition() {
    slide.style.transform = `translateX(${-counter * size}px)`;
}

// Bouton suivant
nextBtn.addEventListener('click', () => {
    counter++;
    if (counter >= items.length) {
        counter = 0; // Retour au début
    }
    updateSlidePosition();
});

// Bouton précédent
prevBtn.addEventListener('click', () => {
    counter--;
    if (counter < 0) {
        counter = items.length - 1; // Retour à la fin
    }
    updateSlidePosition();
});

