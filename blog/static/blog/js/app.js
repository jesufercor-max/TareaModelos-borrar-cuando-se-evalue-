// Interacciones sencillas de la aplicación
document.addEventListener('DOMContentLoaded', () => {
  const year = document.querySelector('[data-current-year]');
  if (year) year.textContent = new Date().getFullYear();
  document.querySelectorAll('a[href]').forEach(link => {
    link.addEventListener('click', () => link.classList.add('visitado'));
  });
});
