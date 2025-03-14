let map = null;
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

function init() {
  drawMap();
  getSpaceList();
  $("#spaces-sort-by").change(function () {
    const selectedValue = $(this).val();
    getSpaceList(selectedValue);
  });
}

init();