const stars = document.querySelectorAll('#stars span');
const submitBtn = document.getElementById('submitBtn');
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');
const inputs = document.querySelectorAll('#author, #product, #title, #content');
const form = document.getElementById('reviewForm');
const ratingInput = document.getElementById('rating');   
const productSelect = document.getElementById('product'); 


let starRating = 0;

// 별점 이벤트
stars.forEach((star, i) => {
    star.addEventListener('click', () => {
        starRating = i + 1;
        stars.forEach((s, idx) => s.classList.toggle('active', idx < starRating));
        ratingInput.value = starRating;
        checkFormFilled();
    });
});

// 파일 선택 시 이름 표시
fileInput.addEventListener('change', () => {
    fileName.textContent = fileInput.files[0]?.name || 'No file chosen';
    checkFormFilled();
});

// 입력 내용 감지
inputs.forEach(input => {
    input.addEventListener('input', checkFormFilled);
});

// 제출해야 할 칸 전체가 채워졌는지 검사
function checkFormFilled() {
    const allFilled = Array.from(inputs).every(input => input.value.trim() !== '');
    const fileSelected = fileInput.files.length > 0;
    const starsSelected = starRating > 0;

    if (allFilled && fileSelected && starsSelected) {
        submitBtn.classList.add('active');
        submitBtn.disabled = false;
    } else {
        submitBtn.classList.remove('active');
        submitBtn.disabled = true;
    }
}


// 폼 제출 시 선택한 item_id로 action 설정
form.addEventListener('submit', (e) => {
    const itemId = productSelect.value;

    if (!itemId) {
        alert('상품을 선택하세요.');
        e.preventDefault();
        return;
    }

    form.action = '/write_review/' + encodeURIComponent(itemId);
});
