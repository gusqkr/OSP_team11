
function toggleAnswerForm(id) {

    const summaryDiv = document.getElementById('summary-' + id);
    const detailDiv = document.getElementById('detail-' + id);

    const isOpened = detailDiv.style.display === 'block';

    if (isOpened) {
        detailDiv.style.display = 'none';
        summaryDiv.style.display = 'block';
    } else {
        detailDiv.style.display = 'block';
        summaryDiv.style.display = 'none';
    }
}

    

document.addEventListener("DOMContentLoaded", function() {
    const forms = document.querySelectorAll(".answer-form");

    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const textarea = this.querySelector("textarea[name='answer_text']");
            if (textarea && textarea.value.trim() === "") {
                alert("답변을 입력하세요.");
                event.preventDefault();
            }
        });
    });
});