document.addEventListener("DOMContentLoaded", () => {
  //아이디 중복 확인
  const checkBtn = document.querySelector(".check-btn");
  const idInput = document.querySelector('.input-with-btn input[type="text"]');
  const idGuide = document.querySelector(".input-with-btn").nextElementSibling;

  //임시 아이디 목록
  const existingIds = ["epick1", "epick2", "epick3"];

  checkBtn.addEventListener("click", () => {
    const enteredId = idInput.value.trim();

    if (enteredId === "") {
      idGuide.textContent = "아이디를 입력해주세요.";
      idGuide.style.color = "red";
      return;
    }

    if (existingIds.includes(enteredId)||enteredId.length < 8) {
      idGuide.textContent = "다른 아이디를 입력해주세요.";
      idGuide.style.color = "red";
    }
    else {
      idGuide.textContent = "사용 가능한 아이디입니다.";
      idGuide.style.color = "green";
    }
  });

  //이메일 형식 검증
  const emailInput = document.querySelector('input[type="email"]');
  const emailGroup = document.querySelector(".email-group");

  const emailError = document.createElement("p");
  emailError.className = "error-text";
  emailGroup.appendChild(emailError);

  emailInput.addEventListener("blur", () => {
    const emailValue = emailInput.value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (emailValue && !emailRegex.test(emailValue)) {
      emailError.textContent = "유효한 이메일을 입력해주세요.";
      emailError.style.color = "red";
      emailError.style.fontSize = "13px";
      emailError.style.marginTop = "6px";
    } else {
      emailError.textContent = "";
    }
  });

  //비밀번호 일치 확인
  const pwInputs = document.querySelectorAll('input[type="password"]');
  const pw1 = pwInputs[0];
  const pw2 = pwInputs[1];
  const pwGuide = pw1.closest(".form-group").querySelector(".guide-text");

  const pwMatchError = document.createElement("p");
  pwMatchError.className = "error-text";
  pw2.parentElement.appendChild(pwMatchError);

  pw1.addEventListener("input", () => {
    if (pw1.value && pw1.value.length < 8) {
      pwGuide.textContent = "비밀번호는 8자 이상이어야 합니다.";
      pwGuide.style.color = "red";
    } else {
      pwGuide.textContent = "영문, 숫자 포함 8자 이상 작성해주세요.";
      pwGuide.style.color = "#777";
    }
  });

  pw2.addEventListener("input", () => {
    if (pw2.value && pw1.value !== pw2.value) {
      pwMatchError.textContent = "비밀번호가 일치하지 않습니다.";
      pwMatchError.style.color = "red";
      pwMatchError.style.fontSize = "13px";
      pwMatchError.style.marginTop = "6px";
    } else {
      pwMatchError.textContent = "";
    }
  });


  //회원가입 버튼 활성화
  const signupBtn=document.querySelector(".signup-btn");
  const agreeCheckbox = document.querySelector('.agreement input[type="checkbox"]');

  function updateSignupButtonState() {
  const idValid = idGuide.textContent === "사용 가능한 아이디입니다.";
  const emailValid = emailError.textContent === "";
  const pwLengthValid = pw1.value.length >= 8;
  const pwMatchValid = pw1.value === pw2.value && pw2.value !== "";
  const agreeChecked = agreeCheckbox.checked;
  signupBtn.disabled = !(idValid && emailValid && pwLengthValid && pwMatchValid && agreeChecked);
  }

  [idInput, emailInput, pw1, pw2].forEach(input => {
    input.addEventListener("input", updateSignupButtonState);
  });
  checkBtn.addEventListener("click", updateSignupButtonState);
  agreeCheckbox.addEventListener("change", updateSignupButtonState);


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
