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
        showDialog(`
          <div class="display-flex align-items-center justify-content-center" style="padding: 20px 0">
            <div>Are you sure you want to cancel this reservation?</div>
          </div>
        `, () => {
          return new Promise((resolve) => {
            customAjax("POST", `/api/v1/bookings/cancel`, { 'booking_id': reserve.id }).then(() => {
              getReservations();
              showMsg('Cancel Successful', 'success');
            });
            resolve();
          });
        });
      });
      $('#reserve-history').append(newEl);
      const statusEl = newEl.find('.reservation-item-status');
      if (dayjs().isBefore(dayjs(reserve.start_time))) {
        statusEl.text('Not Started');
        statusEl.css('background-color', '#cc9900');
      } else if (dayjs().isBefore(dayjs(reserve.end_time))) {
        statusEl.text('In Progress');
        statusEl.css('background-color', '#336600');
      } else {
        statusEl.text('Expired');
        statusEl.css('background-color', '#cc0000');
      }
      newEl.show();
    }
  });
}

function delFavour(id) {
  showDialog(`
    <div class="display-flex align-items-center justify-content-center" style="padding: 20px 0">
      <div>Are you sure you want to unfavorite this space?</div>
    </div>
  `, () => {
    return new Promise((resolve) => {
      customAjax("POST", '/api/del-favourite', { id }).then(() => {
        getFavourites();
        showMsg('Unfavourite Successful', 'success');
      });
      resolve();
    });
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