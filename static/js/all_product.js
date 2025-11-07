// 하트 클릭 이벤트
const hearts = document.querySelectorAll('.heart');
hearts.forEach(h => {
    h.addEventListener('click', () => {
        h.classList.toggle('active');
        h.textContent = h.classList.contains('active') ? '♥' : '♡';
    });
});

// 포커스 해제 (페이지 로드 시)
window.addEventListener('load', () => {
    if (document.activeElement) {
        document.activeElement.blur();
    }
});
