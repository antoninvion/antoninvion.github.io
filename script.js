const items = document.querySelectorAll('.carousel-item');
let current = 0;

function updateCarousel() {
  items.forEach((item, index) => {
    item.classList.remove('active');
    if (index === current) {
      item.classList.add('active');
    }
  });
  const offset = -current * 320; // 300px image + 2x10px margins
  document.querySelector('.carousel').style.transform = `translateX(${offset}px)`;
}

document.getElementById('prevBtn').addEventListener('click', () => {
  current = (current - 1 + items.length) % items.length;
  updateCarousel();
});

document.getElementById('nextBtn').addEventListener('click', () => {
  current = (current + 1) % items.length;
  updateCarousel();
});

// Initial
updateCarousel();


