const fileInput = document.getElementById('img');
const plaaceholder = document.querySelector('.photo-placeholder');

document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();

    if (fileInput.files.length === 0){
        alert('상품 사진을 첨부해 주세요.');
        plaaceholder.style.border = '2px solid red';
    }
    else {
        event.target.submit();
    }
});

fileInput.addEventListener('change', function(){
    if (fileInput.files.length > 0) {
        plaaceholder.style.border = '2px solid green';
    }
});