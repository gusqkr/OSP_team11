const fileInput = document.getElementById('img');
const placeholder = document.querySelector('.photo-placeholder');
const submitBtn = document.getElementById('submitBtn');

const inputs = document.querySelectorAll('#name, #addr, #price, #description');

fileInput.addEventListener('change', function() {
    if (fileInput.files.length > 0) {
        placeholder.style.border = '2px solid green'; 
    }
    checkFormFilled();
});

inputs.forEach(input => {
    input.addEventListener('input', checkFormFilled);
});

function checkFormFilled() {
    const allTextFilled = Array.from(inputs).every(input => input.value.trim() !== '');
    const fileSelected = fileInput.files.length > 0;

    if (allTextFilled && fileSelected) {
        submitBtn.classList.add('active'); 
        submitBtn.disabled = false;        
    } else {
        submitBtn.classList.remove('active'); 
        submitBtn.disabled = true;            
    }
}