// Preserved frontend interactions for the Django-rendered homepage.
const cursor = document.getElementById('cursor');
const ring = document.getElementById('cursorRing');
let mouseX = 0;
let mouseY = 0;
let ringX = 0;
let ringY = 0;

document.addEventListener('mousemove', (event) => {
  mouseX = event.clientX;
  mouseY = event.clientY;
});

function animateCursor() {
  if (cursor && ring) {
    cursor.style.left = `${mouseX}px`;
    cursor.style.top = `${mouseY}px`;
    ringX += (mouseX - ringX) * 0.12;
    ringY += (mouseY - ringY) * 0.12;
    ring.style.left = `${ringX}px`;
    ring.style.top = `${ringY}px`;
  }
  requestAnimationFrame(animateCursor);
}
animateCursor();

const reveals = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });
reveals.forEach((element) => observer.observe(element));

const toast = document.getElementById('toast');
if (toast && toast.dataset.message) {
  toast.classList.add('show', toast.dataset.type || 'success');
  window.setTimeout(() => toast.classList.remove('show'), 4000);
}
