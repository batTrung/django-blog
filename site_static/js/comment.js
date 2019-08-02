$(function(){
	var loadForm = function(){
		var el = $(this);

		$.ajax({
			url: el.attr('data-url'),
			dataType: 'json',
			type: 'get',
			beforeSend: function(){
				$('#js-write-comment').hide();
			},
			success: function(data){
				$('.show-comment-form').html(data.html_comment_form);
			}
		})

		return false
	}

	var saveForm = function(){
		var el = $(this)

		$.ajax({
			url: el.attr("action"),
			dataType: 'json',
			type: 'post',
			data: el.serialize(),
			success: function(data){
				$('.comment-list').html(data.html_comment);
				$('#js-comment-form')[0].reset();
				$('#js-comment-form').hide();
				$('#js-write-comment').fadeIn(500);

			}
		})

		return false
	}

	var loadReplyForm = function(){
		var el = $(this);
		var elShow = el.attr('id-show');

		$.ajax({
			url: el.attr('data-url'),
			dataType: 'json',
			type: 'get',
			success: function(data){
				$('#js-reply-form').remove()
				$(elShow).append(data.html_reply_form);
			}
		})

		return false
	}

	var saveReplyForm = function(){
		var el = $(this);
		var elShow = $('#js-reply').attr('id-show');

		$.ajax({
			url: el.attr("action"),
			dataType: 'json',
			type: 'post',
			data: el.serialize(),
			success: function(data){
				alert('success')
				$(elShow).html(data.html_replies);
			}
		})

		return false
	}

	$('.comments').on('click', '#js-comment', loadForm)
	$('.comments').on('submit', '#js-comment-form', saveForm)


	$('.comments').on('click', '#js-reply', loadReplyForm)
	$('.comments').on('submit', '#js-reply-form', saveReplyForm)


})