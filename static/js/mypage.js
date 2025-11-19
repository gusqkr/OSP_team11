document.addEventListener("DOMContentLoaded", () => {
  //비밀번호 일치 확인
  const pwInputs = document.querySelectorAll('input[type="password"]');
  const pw1 = pwInputs[0];
  const pw2 = pwInputs[1];

  // guide-text를 form-group 다음 형제로 찾기
  const pwGuide = pw1.closest(".form-group").nextElementSibling;

  // 1) 첫 번째 비밀번호 유효성 검사
  pw1.addEventListener("input", () => {
    if (pw1.value && pw1.value.length < 8) {
      pwGuide.textContent = "비밀번호는 8자 이상이어야 합니다.";
      pwGuide.style.color = "red";
    } else {
      pwGuide.textContent = "영문, 숫자 포함 8자 이상 작성해주세요.";
      pwGuide.style.color = "#777";
    }
  });

  // 2) 두 번째 비밀번호 일치 검사
  pw2.addEventListener("input", () => {
    // 첫 번째 비밀번호 조건이 맞지 않으면 일치 검사 안함
    if (pw1.value.length < 8) return;

    if (pw2.value && pw1.value !== pw2.value) {
      pwGuide.textContent = "비밀번호가 일치하지 않습니다.";
      pwGuide.style.color = "red";
    } else {
      pwGuide.textContent = "영문, 숫자 포함 8자 이상 작성해주세요.";
      pwGuide.style.color = "#777";
    }
  });

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
