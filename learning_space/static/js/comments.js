function init() {
  const id = getUrlId();
  $('#view-reserve-btn').click(() => {
    goTo(`/reserve/${getUrlId()}`);
  });
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
  getComments(id);
}

function getComments(id) {
  customAjax("GET", `/api/comments`, { space_id: id }).then(({ data }) => {
    const comments = data ?? [];
    $('#user-comments-container').empty();
    for (const comment of comments) {
      const newEl = $('#user-comment-template').clone();
      newEl.removeAttr('id');
      newEl.find('.username').html(`
        <div class="comment-user-name">
          <icon-user class="comment-icon-user"></icon-user>
          <span>${comment.nickname}</span>
        </div>
      `);
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
  showGlobalLoading();
  customAjax("POST", `/api/comments/submit`, params).then(() => {
    $('#comment-textarea').val('');
    getComments(getUrlId());
    showMsg('Comment successful', 'success');
    getSpaceDetail(getUrlId());
    hideGlobalLoading();
  });
}

init();