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
    for (space of spaceList) {
      const newElement = $('#space-item-template').clone();
      newElement.show();
      newElement.removeAttr('id');
      newElement.find('.space-name').text(space.space_name);
      newElement.find('.space-rating').html(scoreToStars(space.score));
      $('#space-container').append(newElement);
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

let currentMapCenter = { lat: 55.8668275, lng: -4.2514823 };