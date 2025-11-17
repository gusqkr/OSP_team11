document.addEventListener("DOMContentLoaded", function() {
    const dataRows = document.querySelectorAll(".data-row");
    dataRows.forEach(row => {
        row.addEventListener("click", function() {
            this.classList.toggle("expanded");
            closeOtherRows(this);
        });
    });

    const answerForms = document.querySelectorAll(".answer-form");
    answerForms.forEach(form => {
        form.addEventListener("click", function(event) {
            event.stopPropagation();
        });

        form.addEventListener("submit", function(event) {
            event.preventDefault();

            const textarea = this.querySelector("textarea[name='answer_content']");
            const answerContent = textarea.value.trim();
    
            if (answerContent === "") {
                alert("답변 내용을 입력해주세요.");
                return;
            }
            const detailContent = this.closest(".detail-content");
            if (detailContent) {
                const answerDisplayArea = detailContent.querySelector(".seller-answer");

                const newAnswerHTML = `
                    <div class="seller-answer">
                        <strong>A:</strong>
                        <p>${answerContent}</p>
                    </div>
                `;
                answerDisplayArea.innerHTML = newAnswerHTML;
                textarea.value = "";
                this.style.display = "none";
            }
    });
    });
    
    function closeOtherRows(currentOpenRow) {
        document.querySelectorAll('.detail-row').forEach(row => {
            if (row !== currentOpenRow && row.classList.contains('expanded')) {
                row.classList.remove('expanded');
            }
    });
    }
});