function customAjax(type, url, data, headers = {}) {
  return new Promise((resolve, reject) => {
    $.ajax({
      type: type,
      url: url,
      data: data,
      beforeSend: function (xhr) {
        for (let key in headers) {
          xhr.setRequestHeader(key, headers[key]);
        }
      },
      success: function (response) {
        resolve(response);
      },
      error: function (xhr, status, error) {
        reject(error);
      }
    });
  });
}