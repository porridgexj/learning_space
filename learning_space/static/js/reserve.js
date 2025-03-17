const id = getUrlId();

function init() {
  $('#view-comments-btn').attr('href', `/comments/${id}`);
  getSpaceDetail(id);
  getSpaceList();
  getSeats(id);
  $("#spaces-sort-by").change(function () {
    const selectedValue = $(this).val();
    getSpaceList(selectedValue);
  });
  $('#favourite-btn').click(() => {
    addFavour(getLocal('userid'), getUrlId());
  });
}

function getSpaceDetail(id) {
  customAjax("GET", `/api/v1/classrooms/${id}`).then(res => {
    const { space_name, score, description, seat_num } = res;
    $('#space-name').text(space_name);
    $('#space-score').html(scoreToStars(score));
    $('#space-desc-content').text(description);
  });
}

function getSeats(id) {
  customAjax("GET", `/api/v1/classrooms/${id}/bookings`).then(res => {
    const seatList = res?.seat_status_list ?? [];
    $('#seats-container').empty();
    for (const seat of seatList) {
      const seatColors = { 1: 'rgba(81, 74, 56, 1)', 2: 'red' }
      const newEl = $('#seat-option').clone();
      newEl.removeAttr('id');
      newEl.attr('seat-id', seat.index);
      newEl.show();
      if (seat.status !== 0) {
        newEl.css({ 'color': seatColors[seat.status] });
        newEl.removeClass('seat-option-hover');
      }
      newEl.click(() => {
        if (seat.status === 0) {
          showDialog(`
            <div class="confirm-reserve">
              <div><span class="bold margin-r-4">Space:</span>${$('#space-name').text()}</div>
              <div><span class="bold margin-r-4">Seat No:</span>${seat.index}</div>
              <div>
                <span class="bold margin-r-4">Duration:</span>
                <select class="reserve-duration" duration-select-id="${id}">
                  <option value="2">2</option>
                  <option value="3">3</option>
                  <option value="4">4</option>
                  <option value="5">5</option>
                  <option value="6">6</option>
                </select>
                <span>hours</span>
              </div>
              <div class="bold">Are you sure you want to reserve this seat?</div>
            </div>
          `, () => {
            const duration = $(`[duration-select-id="${id}"]`).val();
            reserveSeat(seat.index, duration);
          });
        }
      });
      newEl.append(`<span class="seat-option-index">${seat.index}</span>`);
      $('#seats-container').append(newEl);
    }
  });
}

function reserveSeat(seatId, duration) {
  const params = {
    "user_email": getLocal('email'),
    "classroom_id": id,
    "seat_no": seatId,
    "start_time": dayjs().format('YYYY-MM-DD HH:mm:ss'),
    "end_time": dayjs().add(duration, 'hour').format('YYYY-MM-DD HH:mm:ss'),
  }
  customAjax("POST", `/api/v1/bookings`, params).then(res => {
    getSeats(id);
    showMsg('Reserve success', 'success');
  })
}

init();