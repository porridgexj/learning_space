function init() {
  $("input[name='email']").val(getLocal('email'));
  initLoginForm();
  initRegisterForm();
}

function initLoginForm() {
  $("#login-form").submit(function (event) {
    event.preventDefault();
    if (this.checkValidity()) {
      const username = $("input[name='email']").val();
      const password = $("input[name='password']").val();
      login(username, password);
    }
  });
}

function initRegisterForm() {
  $("#register-form").submit(function (event) {
    event.preventDefault();
    if (this.checkValidity()) {
      const email = $("input[name='register-email']").val().trim();
      const nickname = $("input[name='register-nickname']").val().trim();
      const passwd = $("input[name='register-pw']").val().trim();
      const confirmPasswd = $("input[name='register-confirm-pw']").val().trim();
      if (passwd !== confirmPasswd) {
        showMsg("Passwords do not match");
        return;
      }
      register({ email: email, nickname: nickname, passwd: passwd });
    }
  });
}

function login(email, passwd) {
  customAjax('POST', '/api/login', { email: email, password: passwd }).then(({ data }) => {
    const { userid, email, nickname } = data ?? {};
    setLocal('userid', userid);
    setLocal('email', email);
    setLocal('nickname', nickname.slice(0, 10));
    goTo('/');
  }).catch(() => {
    showMsg('Login failed');
  })
}

function register(data) {
  const { email, nickname, passwd } = data;
  customAjax('POST', '/api/register', { email: email, nickname: nickname, password: passwd }).then(() => {
    $("input[name='register-email']").val('');
    $("input[name='register-nickname']").val('');
    $("input[name='register-pw']").val('');
    $("input[name='register-confirm-pw']").val('');
    showMsg('Register successful', 'success');
  }).catch(res => {
    showMsg(res.message ?? '');
  })
}

init();