document.addEventListener('DOMContentLoaded', () => {

    const likeBtn = document.querySelector('.like');
    if (!likeBtn) return; 

    
    const productId = likeBtn.dataset.productId;
    
    //  productId가 유효한지 확인하는 로직
    if (!productId || productId === 'undefined') {
        console.error("오류: 상품 ID를 찾을 수 없습니다. (productId:", productId, ")");
        // 하트 클릭 이벤트 리스너를 추가하지 않고 종료
        return; 
    }

    const likeCountSpan = likeBtn.querySelector('.like-count');
    const heartSymbolSpan = likeBtn.querySelector('.heart-symbol');
    //const productId = likeBtn.dataset.productId;
    
    let liked = likeBtn.dataset.isLiked === 'true'; 

    likeBtn.addEventListener('click', () => {
        let currentCount = parseInt(likeCountSpan.textContent);
        
        // 현재 상태를 기반으로 서버에 요청할 action 결정
        const action = liked ? 'remove' : 'add'; 

        // 찜하기/찜 취소 요청을 서버에 전송 (AJAX)
        fetch(`/toggle_heart/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ action: action })
        })
        .then(response => {
            if (response.status === 401) { // 401 Unauthorized (로그인 필요)
                return response.json().then(data => {
                    if (data.login_required) {
                        alert(data.message || "로그인이 필요합니다.");
                        window.location.href = '/login?next=' + window.location.pathname; 
                    } else {
                        throw new Error("처리할 수 없는 응답 상태입니다.");
                    }
                });
            }
            if (!response.ok) {
                throw new Error('네트워크 응답이 실패했습니다.');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // 서버 처리 성공 시 UI 업데이트
                if (data.new_status) { // 찜 성공 (new_status: true)
                    currentCount += 1;
                    heartSymbolSpan.textContent = '♥';
                    likeBtn.classList.add('active');
                    liked = true;

                    // 애니메이션 재실행
                    likeBtn.classList.remove('animate-heart');
                    void likeBtn.offsetWidth;
                    likeBtn.classList.add('animate-heart');
                    setTimeout(() => {
                        likeBtn.classList.remove('animate-heart');
                    }, 200);

                } else { // 찜 취소 성공 (new_status: false)
                    currentCount = Math.max(0, currentCount - 1);
                    heartSymbolSpan.textContent = '♡';
                    likeBtn.classList.remove('active');
                    liked = false;
                }
                
                likeCountSpan.textContent = currentCount; // 카운트 업데이트
            } else {
                alert(data.message || '처리 중 오류가 발생했습니다.'); 
            }
        })
        .catch(error => {
            console.error('하트 토글 오류:', error);
            alert('요청 처리 중 오류가 발생했습니다.');
        });
    });
});

const purchaseForm = document.getElementById('purchaseForm');
const buyButton = document.getElementById('buy-button');
const buyModal = document.getElementById('buyModal');
const confirmPurchase = document.getElementById('confirmPurchase');
const cancelPurchase = document.getElementById('cancelPurchase');

buyButton.addEventListener('click', ()=>{
    buyModal.classList.add('active');
});

function closeModal() {
    buyModal.classList.remove('active');
}
cancelPurchase.addEventListener('click',closeModal);

confirmPurchase.addEventListener('click', ()=>{
    closeModal();
    purchaseForm.submit();
})
