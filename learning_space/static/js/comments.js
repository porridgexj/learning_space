function init() {
  const id = getUrlId();
  $('#view-reserve-btn').attr('href', `/reserve/${id}`);
  for (let i = 5; i >= 1; i -= 0.5) {
    $("#rating-select").append(`<option value="${i}">${i}</option>`);
  }
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
  });
}

init();