const id = getUrlId();

function init() {
  $('#view-comments-btn').click(() => {
    goTo(`/comments/${getUrlId()}`);
  })
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
              <div class="unavailable-time-title">Unavailable Time Slots on <span class="selected-date"></span></div>
              <div id="unavailable-time-list" class="unavailable-time-list"></div>
            </div>
            <div>
              <span class="bold margin-r-4">Start Time:</span>
              <input type="datetime-local" class="it-datetime-input reserve-start-time">
            </div>
            <div>
              <span class="bold margin-r-4" style="margin-right: 12px">End Time:</span>
              <input type="datetime-local" class="it-datetime-input reserve-end-time">
            </div>
            <div class="bold">Confirm reservation for this seat?</div>
          </div>
        `, (newEl) => {
          return new Promise((resolve, reject) => {
            const startTime = newEl.find('.reserve-start-time').val();
            const endTime = newEl.find('.reserve-end-time').val();
            const dayjsStartTime = dayjs(startTime);
            const dayjsEndTime = dayjs(endTime);
            if (!dayjsStartTime.isSame(dayjsEndTime, 'day')) {
              showMsg('Start time and end time must be on the same day');
              reject();
              return;
            }
            if (dayjsStartTime.isAfter(dayjsEndTime) || dayjsStartTime.isSame(dayjsEndTime)) {
              showMsg('Start time cannot be later than or equal to the end time');
              reject();
              return;
            }
            reserveSeat(seat.index, startTime, endTime, newEl).then(() => {
              resolve();
            }).catch(() => {
              reject();
            });
          });
        }, (newEl) => {
          const startTimeSel = newEl.find('.reserve-start-time');
          const endTimeSel = newEl.find('.reserve-end-time');
          newEl.find('.selected-date').text(dayjs().format('DD/MM/YYYY'));
          startTimeSel.val(dayjs().format("YYYY-MM-DDTHH:mm"));
          endTimeSel.val(dayjs().add(2, 'hour').format("YYYY-MM-DDTHH:mm"));
          getUnavailableTime(id, seat.index, dayjs().format("YYYY-MM-DD"));
          startTimeSel.on("change", function () {
            let newVal = $(this).val();
            newEl.find('.selected-date').text(dayjs(newVal).format('DD/MM/YYYY'));
            getUnavailableTime(id, seat.index, dayjs(newVal).format("YYYY-MM-DD"));
          });
        });
      });
      newEl.append(`<span class="seat-option-index">${seat.index}</span>`);
      $('#seats-container').append(newEl);
    }
  });
}

function reserveSeat(seatId, startTime, endTime, dialog) {
  return new Promise((resolve, reject) => {
    const params = {
      "user_email": getLocal('email'),
      "classroom_id": id,
      "seat_no": seatId,
      "start_time": dayjs(startTime).format('YYYY-MM-DD HH:mm:ss'),
      "end_time": dayjs(endTime).format('YYYY-MM-DD HH:mm:ss'),
    }
    dialog.find('.btn-loading-mask').show();
    customAjax("POST", `/api/v1/bookings`, params).then(res => {
      showMsg('Reserve success', 'success');
      resolve();
    }).catch(res => {
      showMsg(res.message);
      reject();
    }).finally(() => {
      dialog.find('.btn-loading-mask').hide();
    });
  });
}

function getUnavailableTime(spaceid, seatid, date) {
  const query = {
    classroom_id: spaceid,
    seat_no: seatid,
    date: date,
  }
  showGlobalLoading();
  $('#unavailable-time-list').empty();
  customAjax("GET", `/api/v1/classrooms/bookingslots`, query).then(({ booked_slots }) => {
    timeListHtml = '';
    if (booked_slots.length === 0) {
      timeListHtml += `<div>No Data</div>`;
    } else {
      for (const time of booked_slots ?? []) {
        timeListHtml += `<div>${time}</div>`;
      }
    }
    $('#unavailable-time-list').html(timeListHtml);
    hideGlobalLoading();
  }).catch(() => {
    hideGlobalLoading();
  })
}

init();