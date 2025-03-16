function getReservations() {
  customAjax("GET", '/api/bookings', { id: getLocal('userid') }).then(({ data }) => {
    $('#reserve-history').empty();
    for (const reserve of data) {
      const newEl = $('#reserve-item-template').clone();
      newEl.removeAttr('id');
      newEl.find('.space-name').text(reserve.space__space_name);
      newEl.find('.seat-id-value').text(`${reserve.seat_no}`);
      newEl.find('.start-time-value').text(`${dayjs(reserve.start_time).format('YYYY-MM-DD HH:mm:ss')}`);
      newEl.find('.end-time-value').text(`${dayjs(reserve.end_time).format('YYYY-MM-DD HH:mm:ss')}`);
      newEl.find('.details-btn-link').attr('href', `/reserve/${reserve.space__id}`);
      newEl.find('.cancel-btn').click(() => {
        customAjax("POST", `/api/v1/bookings/cancel`, { 'booking_id': reserve.id }).then(() => {
          getReservations();
        });
      });
      $('#reserve-history').append(newEl);
      newEl.show();
    }
  });
}

function delFavour(id) {
  customAjax("POST", '/api/del-favourite', { id }).then(() => {
    getFavourites();
  });
}

function getFavourites() {
  customAjax("GET", '/api/favourites', { id: getLocal('userid') }).then(({ data }) => {
    const favours = data ?? [];
    $('#favourites-container').empty();
    for (const favour of favours) {
      const newEl = $('#favourite-template').clone();
      newEl.removeAttr('id');
      newEl.find('.space-name').text(favour.space__space_name);
      newEl.find('.delete-btn').click((e) => {
        e.stopPropagation();
        delFavour(favour.id);
      });
      newEl.click(() => {
        goTo('/reserve/' + favour.space__id);
      });
      $('#favourites-container').append(newEl);
      newEl.show();
    }
  });
}

function init() {
  getReservations();
  getFavourites();
}

init();