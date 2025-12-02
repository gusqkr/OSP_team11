// 하트 클릭 이벤트
const hearts = document.querySelectorAll('.heart');
hearts.forEach(h => {
    h.addEventListener('click', () => {
        const productId = h.dataset.productId;
        const isCurrentlyActive = h.classList.contains('active');
        const action = isCurrentlyActive ? 'remove' : 'add';

        // 찜하기/찜 취소 요청을 서버에 전송
        fetch(`/toggle_heart/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ action: action })
        })
        .then(response => {
            if (response.status === 401) { //로그인 필요
                // 서버에서 'login_required: true'를  응답할 경우
                return response.json().then(data => {
                    if (data.login_required) {
                        alert(data.message || "로그인이 필요합니다.");
                        const nextUrl = encodeURIComponent(window.location.pathname);
                        window.location.href = `/login?next=${nextUrl}&need_login=1`; 
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
                if (data.new_status) { // 찜 성공
                    h.classList.add('active');
                    h.textContent = '❤︎ ';
                } else { // 찜 취소 성공
                    h.classList.remove('active');
                    h.textContent = '♡';
                }
                console.log(data.message);
            } else {
                alert(data.message || '처리 중 오류가 발생했습니다.');
            }
        })
    });
});

// 포커스 해제 
window.addEventListener('load', () => {
    if (document.activeElement) {
        document.activeElement.blur();
    }
});