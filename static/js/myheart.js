
/*
        const hearts = document.querySelectorAll('.heart');

        hearts.forEach(heart => {
            heart.addEventListener('click', () => {
                // 하트 active(초록색) 상태 —> 찜 해제
                if (heart.classList.contains('active')) {
                    heart.classList.remove('active');
                    // 해당 하트가 속한 상품 카드 제거
                    const productCard = heart.closest('.product-card');
                    if (productCard) {
                        productCard.remove();
                    }
                } else {
                    // 만약 하트가 비어있던 경우 다시 찜하기 가능
                    heart.classList.add('active');
                }
            });
        });*/
document.addEventListener('DOMContentLoaded', () => {
    const hearts = document.querySelectorAll('.heart');

    hearts.forEach(heart => {
        heart.addEventListener('click', (e) => {
            // 상품 상세 페이지로 이동하지 않게 조정
            e.preventDefault();
            e.stopPropagation();

            const productId = heart.dataset.productId; // 상품 id가져옴
            const action = 'remove'; //찜 목록에서는 삭제만 

            // 서버통신
            fetch(`/toggle_heart/${productId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ action: action }) //{action:'remove'}
            })
            .then(response => {
                if (response.status === 401) {
                    alert('로그인이 필요합니다.');
                    window.location.href = '/login';
                    return;
                }
                return response.json();
            })
            .then(data => {
                if (data && data.success) {
                    // 찜 해제 성공 시 화면에서 카드 제거
                    const productCard = heart.closest('.product-card');
                    if (productCard) {
                        productCard.remove();
                    }
                    
                    // (선택사항) 모든 카드가 지워졌을 때 새로고침하거나 메시지를 표시하려면 여기에 추가 로직 작성
                    const grid = document.querySelector('.product-grid');
                    if (grid && grid.children.length === 0) {
                        location.reload(); // 페이지를 새로고침하여 '없음' 메시지 표시
                    }
                } else {
                    alert(data.message || '오류가 발생했습니다.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('요청 처리 중 오류가 발생했습니다.');
            });
        });
    });
});