// portfolio.js (新ファイル)
document.querySelector('#info-btn').addEventListener('click', () => {
  document.querySelector('#info-text').classList.toggle('hidden');
});

images.forEach(img => {
  img.addEventListener("click", () => {
    modal.classList.add("show"); // ← displayじゃなくクラス付与
    modalImg.src = img.src;
  });
});

closeBtn.addEventListener("click", () => {
  modal.classList.remove("show");
});

modal.addEventListener("click", (e) => {
  if (e.target === modal) modal.classList.remove("show");
});
