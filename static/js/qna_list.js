document.addEventListener("DOMContentLoaded", function() {
    const dataRows = document.querySelectorAll(".data-row");
    dataRows.forEach(row => {
        row.addEventListener("click", function() {
            this.classList.toggle("expanded");
            closeOtherRows(this);
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