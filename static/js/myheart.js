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
        });
