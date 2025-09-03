// ============================
// モーダル処理
// ============================
const modal    = document.getElementById('modal');
const modalImg = document.getElementById('modal-img');
const images   = document.querySelectorAll('.work-image');
const closeBtn = document.querySelector('.close');

if (modal && modalImg && images.length) {
  images.forEach(img => {
    img.addEventListener('click', () => {
      modal.classList.add('show');
      modalImg.src = img.src;
      modalImg.alt = img.alt || '';
    });
  });
}

if (closeBtn) {
  closeBtn.addEventListener('click', () => modal.classList.remove('show'));
}

if (modal) {
  modal.addEventListener('click', (e) => {
    if (e.target === modal) modal.classList.remove('show');
  });
}

// ============================
// フェードイン処理
// ============================
const fadeElems = document.querySelectorAll('.fadein');

const runFadeIn = () => {
  fadeElems.forEach(el => {
    const rect = el.getBoundingClientRect();
    if (rect.top < window.innerHeight - 50) {
      el.classList.add('show');
    }
  });
};

// 読み込み時とスクロール時に実行
window.addEventListener('load', runFadeIn);
window.addEventListener('scroll', runFadeIn);
