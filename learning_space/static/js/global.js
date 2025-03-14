function customAjax(type, url, data, headers = {}) {
  const baseUrl = window.location.origin;
  return new Promise((resolve, reject) => {
    $.ajax({
      type: type,
      url: baseUrl + url,
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

let currentMapCenter = { lat: 55.8668275, lng: -4.2514823 };