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
      error: function (xhr, status, error) {
        reject(xhr.responseJSON);
      }
    });
  });
}

function scoreToStars(score) {
  let starsHtml = "";
  let starsNum = 0;
  for (let i = 1; i <= score; i++) {
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
  starsHtml += `<span class="space-list-rating">${(Math.floor(Number(score) * 10) / 10).toFixed(1)}</span>`;
  return starsHtml;
}

function focusMarker(id) {
  const marker = markers[id];
  if (marker) {
    map.flyTo(marker.getLatLng(), 17, {
      animate: true,
      duration: 0.4
    });
    marker.openPopup();
  }
}

function addSpaceIcon(space, lat, lng) {
  const { id, space_name,
    score, distance
  } = space;
  const mapIconSpace = L.divIcon({
    className: 'map-icon map-icon-space',
    html: `
      <svg viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
        <path fill="currentColor" d="M973.142857 273.142857q22.857143 32.571429 10.285714 73.714286l-157.142857 517.714286q-10.857143 36.571429-43.714285 61.428571T712.571429 950.857143H185.142857q-44 0-84.857143-30.571429T43.428571 845.142857q-13.714286-38.285714-1.142857-72.571428 0-2.285714 1.714286-15.428572t2.285714-21.142857q0.571429-4.571429-1.714285-12.285714t-1.714286-11.142857q1.142857-6.285714 4.571428-12t9.428572-13.428572T66.285714 673.714286q13.142857-21.714286 25.714286-52.285715t17.142857-52.285714q1.714286-5.714286 0.285714-17.142857t-0.285714-16q1.714286-6.285714 9.714286-16t9.714286-13.142857q12-20.571429 24-52.571429t14.285714-51.428571q0.571429-5.142857-1.428572-18.285714t0.285715-16q2.285714-7.428571 12.571428-17.428572t12.571429-12.857143q10.857143-14.857143 24.285714-48.285714T230.857143 234.857143q0.571429-4.571429-1.714286-14.571429t-1.142857-15.142857q1.142857-4.571429 5.142857-10.285714t10.285714-13.142857 9.714286-12q4.571429-6.857143 9.428572-17.428572t8.571428-20 9.142857-20.571428 11.142857-18.285715 15.142858-13.428571 20.571428-6.571429T354.285714 76.571429l-0.571428 1.714285q21.714286-5.142857 29.142857-5.142857h434.857143q42.285714 0 65.142857 32t10.285714 74.285714l-156.571428 517.714286q-20.571429 68-40.857143 87.714286T622.285714 804.571429H125.714286q-15.428571 0-21.714286 8.571428-6.285714 9.142857-0.571429 24.571429 13.714286 40 82.285715 40h527.428571q16.571429 0 32-8.857143t20-23.714286l171.428572-564q4-12.571429 2.857142-32.571428 21.714286 8.571429 33.714286 24.571428z m-608 1.142857q-2.285714 7.428571 1.142857 12.857143t11.428572 5.428572h347.428571q7.428571 0 14.571429-5.428572T749.142857 274.285714l12-36.571428q2.285714-7.428571-1.142857-12.857143t-11.428571-5.428572H401.142857q-7.428571 0-14.571428 5.428572T377.142857 237.714286z m-47.428571 146.285715q-2.285714 7.428571 1.142857 12.857142t11.428571 5.428572h347.428572q7.428571 0 14.571428-5.428572T701.714286 420.571429l12-36.571429q2.285714-7.428571-1.142857-12.857143t-11.428572-5.428571H353.714286q-7.428571 0-14.571429 5.428571T329.714286 384z"></path>
      </svg>
    `,
    iconAnchor: [15, 15],
  });
  const marker = L.marker([lat, lng], { icon: mapIconSpace });
  const popupContent = `
    <div class="space-popup">
      <div class="space-popup-name">${space_name}</div>
      <div class="space-score-distance">
        <span class="display-flex align-items-center">${scoreToStars(score)}</span>
        <span class="display-flex align-items-center">${distance.toFixed(1)} Miles</span>
      </div>
      <button id="popup-btn-${id}" class="it-btn space-popup-button">Book Seat</button>
    </div>
  `;
  marker.bindPopup(popupContent, { offset: L.point(0, -8) });
  marker.on("popupopen", function () {
    document.getElementById(`popup-btn-${id}`).addEventListener("click", function () {
      goTo(`/reserve/${id}`);
    });
  });
  marker.addTo(map);
  markers[id] = marker;
}

const markers = {};
function getSpaceList(sortBy = 'distance') {
  let spaceList = [];
  getPosition().then(() => {
    const params = {
      sort_by: sortBy,
      longitude: userPosition.lng,
      latitude: userPosition.lat,
    }
    showGlobalLoading();
    customAjax('GET', '/api/v1/classrooms', params).then(res => {
      spaceList = res;
      globalSpaceList = spaceList;
      $('#space-container').empty();
      for (let [index, space] of spaceList.entries()) {
        const newEl = $('#space-item-template').clone();
        newEl.show();
        newEl.removeAttr('id');
        newEl.attr('space-id', space.id);
        newEl.find('.space-name').text(space.space_name);
        newEl.find('.space-rating').html(scoreToStars(space.score));
        newEl.click(() => {
          if (window.location.href.includes('/reserve') || window.location.href.includes('/comments')) {
            refreshReserve(space.id);
          } else {
            focusMarker(space.id);
          }
        });
        newEl.find('.space-item-index').text(index + 1);
        newEl.find('.space-item-distance').text(`${space.distance.toFixed(1)} Miles`);
        $('#space-container').append(newEl);
        if (map) addSpaceIcon(space, space.latitude, space.longitude);
      }
      $('#space-container').scrollTop(0);
      hideGlobalLoading();
    }).catch((e) => {
      console.log(e);
      hideGlobalLoading();
    });
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
  newMsg.find("#global-message-text").html(text);
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

function getSpaceInfo(id) {
  return globalSpaceList.find(space => space.id === id);
}

function addFavour(userid, spaceid) {
  customAjax('POST', '/api/add-favourite', { userid, spaceid }).then(() => {
    showMsg('Added to favourites', 'success');
    getSpaceDetail(spaceid);
  }).catch(() => {
    showMsg('Failed to add to favourites');
  });
}

function delFavour(userid, spaceid) {
  customAjax('POST', '/api/del-favourite', { user_id: userid, space_id: spaceid }).then(() => {
    showMsg('Unfavourite successful', 'success');
    getSpaceDetail(spaceid);
  }).catch(() => {
    showMsg('Failed to remove favourite');
  });
}

function closeDialog(el) {
  anime({
    targets: el[0],
    opacity: [1, 0],
    duration: 200,
    easing: 'easeOutQuad',
    complete: function () {
      el.remove();
    }
  });
}

function showDialog(html, callback, onMounted) {
  const newEl = $('#dialog-template').clone();
  newEl.removeAttr('id');
  newEl.css({ opacity: 0 });
  newEl.find('.dialog-close').click(() => {
    closeDialog(newEl);
  });
  newEl.find('.dialog-confirm-button').click(() => {
    callback(newEl).then(() => {
      closeDialog(newEl);
    })
  });
  newEl.find('.dialog-content').html(html);
  if (onMounted) onMounted(newEl);
  $('body').append(newEl);
  newEl.show();
  anime({
    targets: newEl[0],
    opacity: [0, 1],
    duration: 200,
    easing: 'easeOutQuad'
  });
}

let spaceInfoMap = null;
function initSpaceInfoMap(space) {
  const { space_name, score, latitude, longitude } = space;
  if (spaceInfoMap) spaceInfoMap.remove();
  spaceInfoMap = L.map('space-map-container').setView([latitude, longitude], 16);
  L.tileLayer(mapSource[mapType], {
    minZoom: 9,
    maxZoom: 18,
  }).addTo(spaceInfoMap);
  spaceInfoMap.setMaxBounds(L.latLngBounds(
    L.latLng(56.386542701886306, -4.890747126191855),
    L.latLng(55.32758195350942, -3.355407770723105)
  ));
  const mapIconSpace = L.divIcon({
    className: 'map-icon map-icon-space',
    html: `
      <svg viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
        <path fill="currentColor" d="M973.142857 273.142857q22.857143 32.571429 10.285714 73.714286l-157.142857 517.714286q-10.857143 36.571429-43.714285 61.428571T712.571429 950.857143H185.142857q-44 0-84.857143-30.571429T43.428571 845.142857q-13.714286-38.285714-1.142857-72.571428 0-2.285714 1.714286-15.428572t2.285714-21.142857q0.571429-4.571429-1.714285-12.285714t-1.714286-11.142857q1.142857-6.285714 4.571428-12t9.428572-13.428572T66.285714 673.714286q13.142857-21.714286 25.714286-52.285715t17.142857-52.285714q1.714286-5.714286 0.285714-17.142857t-0.285714-16q1.714286-6.285714 9.714286-16t9.714286-13.142857q12-20.571429 24-52.571429t14.285714-51.428571q0.571429-5.142857-1.428572-18.285714t0.285715-16q2.285714-7.428571 12.571428-17.428572t12.571429-12.857143q10.857143-14.857143 24.285714-48.285714T230.857143 234.857143q0.571429-4.571429-1.714286-14.571429t-1.142857-15.142857q1.142857-4.571429 5.142857-10.285714t10.285714-13.142857 9.714286-12q4.571429-6.857143 9.428572-17.428572t8.571428-20 9.142857-20.571428 11.142857-18.285715 15.142858-13.428571 20.571428-6.571429T354.285714 76.571429l-0.571428 1.714285q21.714286-5.142857 29.142857-5.142857h434.857143q42.285714 0 65.142857 32t10.285714 74.285714l-156.571428 517.714286q-20.571429 68-40.857143 87.714286T622.285714 804.571429H125.714286q-15.428571 0-21.714286 8.571428-6.285714 9.142857-0.571429 24.571429 13.714286 40 82.285715 40h527.428571q16.571429 0 32-8.857143t20-23.714286l171.428572-564q4-12.571429 2.857142-32.571428 21.714286 8.571429 33.714286 24.571428z m-608 1.142857q-2.285714 7.428571 1.142857 12.857143t11.428572 5.428572h347.428571q7.428571 0 14.571429-5.428572T749.142857 274.285714l12-36.571428q2.285714-7.428571-1.142857-12.857143t-11.428571-5.428572H401.142857q-7.428571 0-14.571428 5.428572T377.142857 237.714286z m-47.428571 146.285715q-2.285714 7.428571 1.142857 12.857142t11.428571 5.428572h347.428572q7.428571 0 14.571428-5.428572T701.714286 420.571429l12-36.571429q2.285714-7.428571-1.142857-12.857143t-11.428572-5.428571H353.714286q-7.428571 0-14.571429 5.428571T329.714286 384z"></path>
      </svg>
    `,
    iconAnchor: [15, 15],
  });
  const userMarker = L.marker([latitude, longitude], { icon: mapIconSpace }).addTo(spaceInfoMap);
  const popupContent = `
    <div class="space-popup">
      <div class="space-popup-name">${space_name}</div>
      <div class="space-score-distance">
        <span class="display-flex align-items-center">${scoreToStars(score)}</span>
      </div>
    </div>
  `;
  userMarker.bindPopup(popupContent, { offset: L.point(0, -8) });
}

function getSpaceDetail(id) {
  customAjax("GET", `/api/v1/classrooms/${id}`, { user_id: getLocal('userid') }).then(res => {
    const { space_name, score, description, is_favourite, latitude, longitude, img_cover } = res;
    $('#space-name').text(space_name);
    $('#space-score').html(scoreToStars(score));
    $('#space-desc-content').html(`
      <div class="space-desc-inner">
        <div class="space-desc-inner-title">Description:</div>
        <div class="space-desc-inner-text">${description}</div>
      </div>
    `);
    $('#info-cover-wrapper').html(`<img id="space-cover" src=/static/images/space${img_cover}.webp alt="cover"></img>`);
    if (is_reserve_page())
      initSpaceInfoMap(res);
    if (is_favourite === 0) {
      $('#favourite-btn').css({ 'background-color': "rgb(174, 89, 89)" });
      $('#favourite-btn').text('Favourite');
      $('#favourite-btn').removeClass('unfavourite-button-hover');
      $('#favourite-btn').addClass('favourite-button-hover');
      $('#favourite-btn').off('click');
      $('#favourite-btn').click(() => {
        addFavour(getLocal('userid'), getUrlId());
      });
    } else {
      $('#favourite-btn').css({ 'background-color': "rgb(51, 102, 0)" });
      $('#favourite-btn').removeClass('favourite-button-hover');
      $('#favourite-btn').addClass('unfavourite-button-hover');
      $('#favourite-btn').text('Unfavourite');
      $('#favourite-btn').off('click');
      $('#favourite-btn').click(() => {
        delFavour(getLocal('userid'), getUrlId());
      });
    }
  });
}

function getPosition() {
  return new Promise((resolve, reject) => {
    showGlobalLoading();
    if (!userPosition) {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            let latitude = position.coords.latitude;
            let longitude = position.coords.longitude;
            userPosition = { lat: latitude, lng: longitude };
            hideGlobalLoading();
            resolve();
          },
          (error) => {
            userPosition = { lat: 55.86567951095817, lng: -4.2657280003186315 };
            hideGlobalLoading();
            resolve();
          }
        );
      } else {
        userPosition = { lat: 55.86567951095817, lng: -4.2657280003186315 };
        hideGlobalLoading();
        resolve();
      }
    } else {
      hideGlobalLoading();
      resolve();
    }
  });
}

function is_reserve_page() {
  return window.location.pathname.startsWith('/reserve');
}

function refreshReserve(id) {
  if (is_reserve_page()) {
    getSeats(id);
    history.replaceState(null, "", `/reserve/${id}/`);
  } else {
    getComments(id);
    history.replaceState(null, "", `/comments/${id}/`);
  }
  getSpaceDetail(id);
}


let globalLoadingCounter = 0;
let globalLoadingStartTime = Date.now();
const leastInterval = 500;
function showGlobalLoading() {
  globalLoadingCounter += 1;
  if (globalLoadingCounter === 1) {
    $('#global-loading').show();
    globalLoadingStartTime = Date.now();
  }
}

function hideGlobalLoading() {
  globalLoadingCounter -= 1;
  if (globalLoadingCounter < 1) {
    const timeInterval = Date.now() - globalLoadingStartTime;
    if (timeInterval >= leastInterval) {
      $('#global-loading').hide();
    } else {
      setTimeout(() => {
        $('#global-loading').hide();
      }, leastInterval - timeInterval);
    }
  }
}

let userPosition = null;
let msgId = 1;
let msgZIndex = 10000;
let globalSpaceList = [];
let map = null;
let mapType = window.localStorage.getItem('mapType') ?? 'normal';
let mapSource = {
  'normal': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  'satellite': 'https://tiles.stadiamaps.com/tiles/alidade_satellite/{z}/{x}/{y}{r}.png?api_key=c133c1b3-dc26-4883-b995-4358b31c43d4',
};

$('#log-out-button').click(() => {
  logout();
});

$('#header-nickname').text(`Welcome, ${getLocal('nickname')}`);