document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('.login-form');
    const idInput = loginForm.querySelector('input[type="text"]');
    const pwInput = loginForm.querySelector('input[type="password"]');
    const loginBtn = loginForm.querySelector('.login-btn');
    const errorMsg = loginForm.querySelector('.error-msg');

    // 초기 버튼 상태 비활성화
    loginBtn.disabled = true;
    loginBtn.style.backgroundColor = 'rgb(0,72,40,0.5)';

    // 입력값 변경 시마다 체크
    const checkInputs = () => {
        const idFilled = idInput.value.trim() !== '';
        const pwFilled = pwInput.value.trim() !== '';

        if (idFilled && pwFilled) {
            // 둘 다 입력 시 버튼 초록색
            loginBtn.disabled = false;
            loginBtn.style.backgroundColor = 'rgb(0,70,42)'; // 원하는 초록색
            errorMsg.style.display = 'none';
        } else {
            // 하나라도 비어있으면 버튼 비활성
            loginBtn.disabled = true;
            loginBtn.style.backgroundColor = '#ccc';
        }
    };

    // 실시간 입력 체크
    idInput.addEventListener('input', checkInputs);
    pwInput.addEventListener('input', checkInputs);

    //비밀번호 토글 기능
    document.querySelectorAll('.toggle-password').forEach(button => {
      button.addEventListener('click', () => {
        const input = button.parentElement.querySelector('input');
        const img = button.querySelector('.eye-icon');

        if (input.type === 'password') {
          input.type = 'text';
          img.src = '../static/images/eye-on.png';
          img.alt = '비밀번호 숨기기';
        } else {
          input.type = 'password';
          img.src = '../static/images/eye-off.png';
          img.alt = '비밀번호 보기';
        }
      });
    });
});
