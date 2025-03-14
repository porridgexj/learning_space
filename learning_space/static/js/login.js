function init() {
  $("#login-button").click(function () {
    $("#login-form").submit();
  });
  $("#login-form").submit(function (event) {
    event.preventDefault();
    const username = $("input[name='username']").val();
    const password = $("input[name='password']").val();
    console.log("用户名:", username);
    console.log("密码:", password);
  });

  $("#register-button").click(function () {
    $("#register-form").submit();
  });
  $("#register-form").submit(function (event) {
    event.preventDefault();
    // const username = $("input[name='username']").val();
    // const password = $("input[name='password']").val();
    // console.log("用户名:", username);
    // console.log("密码:", password);
  });
}

init();