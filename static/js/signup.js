document.addEventListener("DOMContentLoaded", () => {
  //아이디 중복 확인
  const checkBtn = document.querySelector(".check-btn");
  const idInput = document.querySelector('.input-with-btn input[type="text"]');
  const idGuide = document.querySelector(".input-with-btn").nextElementSibling;

    idInput.addEventListener("input", () => {
      const value = idInput.value.trim();
      const idPattern = /^[A-Za-z0-9]{8,}$/;

      if (idPattern.test(value)) {
        checkBtn.style.backgroundColor = "rgb(0,72,40)";
      } else {
        checkBtn.style.backgroundColor = "#678b76";
      }
    });
    
  checkBtn.addEventListener("click", async () => {
    const enteredId = idInput.value.trim();

    if (enteredId === "") {
    idGuide.textContent = "아이디를 입력해주세요.";
    idGuide.style.color = "red";
    checkBtn.style.backgroundColor = "#678b76";
    updateSignupButtonState();
    return;
  }

  if (enteredId.length < 8) {
    idGuide.textContent = "아이디는 8자 이상이어야 합니다.";
    idGuide.style.color = "red";
    checkBtn.style.backgroundColor = "#678b76";
    updateSignupButtonState();
    return;
  }

  const hasLetter = /[a-zA-Z]/.test(enteredId);
  const hasNumber = /[0-9]/.test(enteredId);

  if (!(hasLetter && hasNumber)) {
    idGuide.textContent = "아이디는 영문과 숫자를 모두 포함해야 합니다.";
    idGuide.style.color = "red";
    checkBtn.style.backgroundColor = "#678b76";
    updateSignupButtonState();
    return;
  }

  const formData = new FormData();
  formData.append("id", enteredId);

  const res = await fetch("/check_id", {
        method: "POST",
        body: formData,
  });

  const data = await res.json();
  idGuide.textContent = data.message;
  idGuide.style.color = data.available ? "green" : "red";

  if (data.available) {
        checkBtn.style.backgroundColor = "rgb(0,72,40)";
  } else {
        checkBtn.style.backgroundColor = "#678b76";
  }

    // 중복확인 후 버튼 활성화 상태 다시 계산
  updateSignupButtonState();
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

  const telInput = document.querySelector('input[name="tel"]');
  const telGuide = document.createElement("p");
  telGuide.className = "error-text";
  telInput.parentElement.appendChild(telGuide);

  telInput.addEventListener("input", () => {
  const tel = telInput.value.trim();

  if (!tel) {
    telGuide.textContent = "";
    updateSignupButtonState();
    return;
  }

  const telRegex = /^010-\d{4}-\d{4}$/;

  if (!telRegex.test(tel)) {
    telGuide.textContent = "전화번호는 010-1234-5678 형식으로 입력해주세요.";
    telGuide.style.color = "red";
  } else {
    telGuide.textContent = "";   
  }

  updateSignupButtonState();
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
  const tel = telInput.value.trim();
  const telValid = (tel === "" || /^010-\d{4}-\d{4}$/.test(tel));  
  signupBtn.disabled = !(idValid && emailValid && pwLengthValid && pwMatchValid && telValid && agreeChecked);
  }

  [idInput, emailInput, pw1, pw2].forEach(input => {
    input.addEventListener("input", updateSignupButtonState);
  });
  checkBtn.addEventListener("click", updateSignupButtonState);
  agreeCheckbox.addEventListener("change", updateSignupButtonState);

});
