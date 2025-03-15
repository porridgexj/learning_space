function customAjax(type, url, data, headers = {}) {
  const baseUrl = window.location.origin;
  return new Promise((resolve, reject) => {
    $.ajax({
      type: type,
      url: baseUrl + url,
      data: type === "GET" ? data : JSON.stringify(data),
      beforeSend: function (xhr) {
        for (let key in headers) {
          xhr.setRequestHeader(key, headers[key]);
        }
      },
      success: function (response) {
        resolve(response);
      },
      error: function (xhr) {
        reject(xhr.responseJSON);
      }
    });
  });
}

function scoreToStars(score) {
  let starsHtml = "";
  let starsNum = 0;
  for (let i = 1; i < score; i++) {
    starsHtml += '<icon-star></icon-star>';
    starsNum++;
  }
  if (Math.ceil(score) > score) {
    starsHtml += '<icon-star-half></icon-star-half>';
    starsNum++;
  }
  for (let i = starsNum; i < 5; i++) {
    starsHtml += '<icon-star-empty></icon-star-empty>';
  }
  return starsHtml;
}

function getSpaceList(sortBy = 'distance') {
  let spaceList = [];
  const isSortByDistance = sortBy === 'distance';
  const params = {
    sort_by: sortBy,
    longitude: isSortByDistance ? currentMapCenter.lng : undefined,
    latitude: isSortByDistance ? currentMapCenter.lat : undefined,
  }
  customAjax('GET', '/api/v1/classrooms', params).then(res => {
    spaceList = res;
    $('#space-container').empty();
    for (let space of spaceList) {
      const newEl = $('#space-item-template').clone();
      newEl.show();
      newEl.removeAttr('id');
      newEl.attr('space-id', space.id);
      newEl.find('.space-name').text(space.space_name);
      newEl.find('.space-rating').html(scoreToStars(space.score));
      newEl.click(() => {
        goTo(`/reserve/${space.id}`);
      });
      $('#space-container').append(newEl);
    }
  }).catch((e) => {
    console.log(e);
  });
}

function getUrlId() {
  const url = new URL(window.location.href);
  const pathSegments = url.pathname.split('/');
  const id = pathSegments[pathSegments.length - 2];
  return id;
}

function goTo(url) {
  window.location.href = url;
}

function setLocal(key, value) {
  window.localStorage.setItem(key, value);
}

function getLocal(key) {
  return window.localStorage.getItem(key);
}

function removeLocal(key) {
  window.localStorage.removeItem(key);
}

function showMsg(text = '', type = 'error') {
  const newMsgId = msgId++;
  const newMsgZIndex = msgZIndex++;
  let bgColor = 'rgb(130, 193, 127)';
  if (type === 'error') {
    bgColor = 'rgb(249, 157, 157)';
  }
  let newMsg = $("#global-message").clone();
  newMsg.attr("msg-id", newMsgId);
  newMsg.find("#global-message-text").text(text);
  newMsg.removeAttr('id');
  let initTop = '-76px';
  let targetTop = '20px';
  newMsg.css({
    "z-index": newMsgZIndex,
    "top": initTop,
    "background": bgColor,
  });
  $("body").append(newMsg);
  newMsg.show();
  console.log(anime());
  anime({
    targets: `[msg-id="${newMsgId}"]`,
    top: [initTop, targetTop],
    duration: 200,
    easing: "easeOutQuad",
    complete: function () {
      setTimeout(function () {
        anime({
          targets: `[msg-id="${newMsgId}"]`,
          top: [targetTop, initTop],
          duration: 200,
          easing: "easeInQuad",
          complete: function () {
            $(`[msg-id="${newMsgId}"]`).remove();
          }
        });
      }, 3000);
    }
  });
}

function logout() {
  customAjax('POST', '/api/logout').finally(() => {
    refresh();
  });
}

function refresh() {
  location.reload();
}

let currentMapCenter = { lat: 55.8668275, lng: -4.2514823 };
let msgId = 1;
let msgZIndex = 1000;

$('#log-out-button').click(() => {
  logout();
});

$('#header-nickname').text(`Welcome, ${getLocal('nickname')}`);