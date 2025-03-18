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
  $('#submit-comment-button').click(() => {
    submitRating();
  });
  getComments();
}

function getComments() {
  customAjax("GET", `/api/comments`, { space_id: getUrlId() }).then(({ data }) => {
    const comments = data ?? [];
    $('#user-comments-container').empty();
    for (const comment of comments) {
      console.log(comment);
      const newEl = $('#user-comment-template').clone();
      newEl.removeAttr('id');
      newEl.find('.username').text(comment.nickname);
      newEl.find('.rating').html(scoreToStars(comment.score));
      newEl.find('.comment').text(comment.comment);
      newEl.find('.created-time-text').text(dayjs(comment.created_time).format('YYYY-MM-DD HH:mm:ss'));
      $('#user-comments-container').append(newEl);
      newEl.show();
    }
  });
}

function submitRating() {
  const params = {
    email: getLocal('email'),
    space_id: getUrlId(),
    score: $('#rating-select').val(),
    comment: $('#comment-textarea').val(),
  }
  if (!params.comment) {
    showMsg('Please write a comment');
    return;
  }
  customAjax("POST", `/api/comments/submit`, params).then(() => {
    $('#comment-textarea').val('');
    getComments();
    showMsg('Comment successful', 'success');
  });
}

init();