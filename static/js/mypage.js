document.addEventListener("DOMContentLoaded", () => {

  const flashMsgElement = document.getElementById("flash-message");

  if (flashMsgElement) {
    const msg = flashMsgElement.getAttribute("data-msg");
    if (msg) {
      alert(msg);
    }
  }
  
  //비밀번호 일치 확인
  const pwInputs = document.querySelectorAll('input[type="password"]');
  const pw1 = pwInputs[0];
  const pw2 = pwInputs[1];

  const pwGuide = document.getElementById("pw-guide");
  const pwMatchError = document.getElementById("pw-match-error");

  // 1) 첫 번째 비밀번호 유효성 검사
  pw1.addEventListener("input", () => {
    const value = pw1.value;
    const hasLetter = /[a-zA-Z]/.test(value);
    const hasNumber = /[0-9]/.test(value);

    if (value) {
      if (value.length < 8) {
        pwGuide.textContent = "비밀번호는 8자 이상이어야 합니다.";
        pwGuide.style.color = "red";
        return;
      }

      if (!(hasLetter && hasNumber)) {
        pwGuide.textContent = "비밀번호는 영문과 숫자를 모두 포함해야 합니다.";
        pwGuide.style.color = "red";
        return;
      }

      pwGuide.textContent = "비밀번호 조건을 만족합니다.";
      pwGuide.style.color = "green";

    } else {
      pwGuide.textContent = "영문, 숫자 포함 8자 이상 작성해주세요.";
      pwGuide.style.color = "#777";
    }

    checkMatch();
  });

function checkMatch() {
    if (pw2.value) { // 값이 있을 때만 검사
        if (pw1.value !== pw2.value) {
            pwMatchError.textContent = "비밀번호가 일치하지 않습니다.";
            pwMatchError.style.color = "red";
        } else {
            pwMatchError.textContent = "비밀번호가 일치합니다."; 
            pwMatchError.style.color = "green"; 
        }
    } else {
        pwMatchError.textContent = ""; 
    }
  }

  pw2.addEventListener("input", checkMatch);

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

  //변경하기 버튼 활성화
  const editBtn=document.querySelector(".edit-btn");
  function updateEditButtonState() {
  const pwMatchValid = (pw1.value === pw2.value) && (pw2.value !== "") && (pw1.value.length >= 8);
  editBtn.disabled = !pwMatchValid ;
  }

  [pw1, pw2].forEach(input => {
    input.addEventListener("input", updateEditButtonState);
  });
  editBtn.addEventListener("click", updateEditButtonState);

});
