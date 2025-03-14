function init() {
  const id = getUrlId();
  getSpaceDetail(id);
  getSpaceList();
  $("#spaces-sort-by").change(function () {
    const selectedValue = $(this).val();
    getSpaceList(selectedValue);
  });
}

function getSpaceDetail(id) {
  customAjax("GET", `/api/v1/classrooms/${id}`).then(res => {
    const { space_name, score, description } = res;
    $('#space-name').text(space_name);
    $('#space-score').html(scoreToStars(score));
    $('#space-desc-content').text(description);
    initSeats();
  });
}

function initSeats() {
  for (let i = 0; i < 30; i++) {
    const newEl = $('#seat-option').clone();
    newEl.removeAttr('id');
    newEl.attr('seat-id', i + 1);
    newEl.show();
    $('#seats-container').append(newEl);
  }
}

init();