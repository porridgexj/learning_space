function drawMap() {
  if (map) map.remove();
  getPosition().then(() => {
    const { lat, lng } = userPosition;
    map = L.map('map-container').setView([lat, lng], 13);
    L.tileLayer(mapSource[mapType], {
      minZoom: 9,
      maxZoom: 18,
    }).addTo(map);
    map.setMaxBounds(L.latLngBounds(
      L.latLng(56.386542701886306, -4.890747126191855),
      L.latLng(55.32758195350942, -3.355407770723105)
    ));
    const mapIconUser = L.divIcon({
      className: 'map-icon map-icon-user',
      html: `
      <svg viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
        <path fill="currentColor" d="M512 512c123.776 0 224-100.224 224-224S635.776 64 512 64a223.936 223.936 0 0 0-224 224C288 411.776 388.224 512 512 512z m0 64c-149.504 0-448 85.76-448 256v128h896v-128c0-170.24-298.496-256-448-256z"></path>
      </svg>
    `,
      iconAnchor: [15, 15],
    });
    const userMarker = L.marker([lat, lng], { icon: mapIconUser }).addTo(map);
    userMarker.bindPopup('You are here', { offset: L.point(0, -8) });
    // map.on('click', function (e) {
    //   console.log(e.latlng.lat, e.latlng.lng, map.getZoom());
    //   L.marker([e.latlng.lat, e.latlng.lng], { icon: mapIconUser }).addTo(map);
    // });
  })
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