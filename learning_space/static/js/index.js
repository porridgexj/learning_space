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

function getSpaceList() {
  const spaceList = Array(20).fill({
    name: 'Space 1',
    rating: '★★★★★',
  });
  $('#space-container').empty();
  for (space of spaceList) {
    const newElement = $('#space-item-template').clone();
    newElement.show();
    newElement.removeAttr('id');
    newElement.find('.space-name').text(space.name);
    newElement.find('.space-rating').text(space.rating);
    $('#space-container').append(newElement);
  }
}

function init() {
  drawMap();
  getSpaceList();
}

init();