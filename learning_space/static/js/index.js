let map = null;
let currentMapCenter = { lat: 55.8668275, lng: -4.2514823 };
let mapType = window.localStorage.getItem('mapType') ?? 'normal';
let mapSource = {
  'normal': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  'satellite': 'https://tiles.stadiamaps.com/tiles/alidade_satellite/{z}/{x}/{y}{r}.png?api_key=c133c1b3-dc26-4883-b995-4358b31c43d4',
};

function drawMap() {
  if (map) map.remove();
  const { lat, lng } = currentMapCenter;
  map = L.map('map-container').setView([lat, lng], 14);
  L.tileLayer(mapSource[mapType], {
    maxZoom: 19,
  }).addTo(map);
}

function scoreToStars(score) {
  let starsHtml = "";
  for (let i = 1; i < score; i++) {
    starsHtml += '<icon-star></icon-star>';
  }
  if (Math.ceil(score) > score) {
    starsHtml += '<icon-star-half></icon-star-half>';
  }
  return starsHtml;
}

function getSpaceList(sortBy = 'distance') {
  let spaceList = [];
  customAjax('GET', 'api/v1/classrooms', {
    sort_by: sortBy,
    longitude: currentMapCenter.lng,
    latitude: currentMapCenter.lat,
  }).then(res => {
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

function init() {
  drawMap();
  getSpaceList();
  $("#spaces-sort-by").change(function () {
    const selectedValue = $(this).val();
    getSpaceList(selectedValue);
  });
}

init();