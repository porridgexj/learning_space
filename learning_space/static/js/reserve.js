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
}

function getSeats(id) {
  customAjax("GET", `/api/v1/classrooms/${id}/bookings`).then(res => {
    const seatList = res?.seat_status_list ?? [];
    $('#seats-container').empty();
    for (const seat of seatList) {
      const newEl = $('#seat-option').clone();
      newEl.removeAttr('id');
      newEl.attr('seat-id', seat.index);
      newEl.show();
      newEl.click(() => {
        showDialog(`
          <div class="confirm-reserve">
            <div><span class="bold margin-r-4">Space:</span>${$('#space-name').text()}</div>
            <div><span class="bold margin-r-4">Seat No:</span>${seat.index}</div>
            <div class="unavailable-time">
              <div class="unavailable-time-title">Unavailable Time Slots on <span class="selected-date">18/03/2025</span></div>
              <div class="unavailable-time-list">
                <div> 14:50 - 20:20 </div>
                <div> 14:50 - 20:20 </div>
                <div> 14:50 - 20:20 </div>
                <div> 14:50 - 20:20 </div>
              </div>
            </div>
            <div>
              <span class="bold margin-r-4">Start time:</span>
              <input type="datetime-local" class="it-datetime-input reserve-start-time">
            </div>
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
            <div class="bold">Confirm reservation for this seat?</div>
          </div>
        `, (newEl) => {
          const duration = $(`[duration-select-id="${id}"]`).val();
          const startTime = newEl.find('.reserve-start-time').val();
          reserveSeat(seat.index, duration, startTime);
        }, (newEl) => {
          const startTimeSel = newEl.find('.reserve-start-time');
          startTimeSel.val(dayjs().format("YYYY-MM-DDTHH:mm"));
          startTimeSel.on("change", function () {
            let newVal = $(this).val();
            newEl.find('.selected-date').text(dayjs(newVal).format('DD/MM/YYYY'));
          });
        });
      });
      newEl.append(`<span class="seat-option-index">${seat.index}</span>`);
      $('#seats-container').append(newEl);
    }
  });
}

function reserveSeat(seatId, duration, startTime) {
  console.log(startTime);
  const params = {
    "user_email": getLocal('email'),
    "classroom_id": id,
    "seat_no": seatId,
    "start_time": dayjs(startTime).format('YYYY-MM-DD HH:mm:ss'),
    "end_time": dayjs().add(duration, 'hour').format('YYYY-MM-DD HH:mm:ss'),
  }
  customAjax("POST", `/api/v1/bookings`, params).then(res => {
    getSeats(id);
    showMsg('Reserve success', 'success');
  })
}

init();