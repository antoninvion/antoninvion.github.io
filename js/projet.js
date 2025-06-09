// Mettre à jour les points actifs au scroll
const sections = document.querySelectorAll('.projet');
const dots = document.querySelectorAll('.fil-rouge .dot');

window.addEventListener('scroll', () => {
  let index = sections.length;

  while(--index && window.scrollY + 100 < sections[index].offsetTop) {}

  dots.forEach(dot => dot.classList.remove('active'));
  dots[index].classList.add('active');
});

