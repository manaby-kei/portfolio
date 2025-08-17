// cafe.js
document.querySelector('#toggle-btn').addEventListener('click', () => {
  document.querySelector('main').classList.toggle('main-bg');
});

const images = ['images/coffee.jpg', 'images/cake.jpg'];
let index = 0;
document.querySelector('#slide-btn').addEventListener('click', () => {
  document.querySelector('#hero-img').src = images[index];
  index = (index + 1) % images.length;
});

setInterval(() => {
  document.querySelector('#hero-img').src = images[index];
  index = (index + 1) % images.length;
}, 5000); // 5秒ごと
