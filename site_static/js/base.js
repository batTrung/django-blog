$(function(){

	var saveProfileForm = function(){
		var el = $(this);
		$.ajax({
			url: el.attr('action'),
			type: 'post',
			dataType: 'json',
			data: el.serialize(),
			success: function(data){
				$('#error').hide();
				if (data.form_valid) {
					$('#myModal').modal("hide")
				} else {
					$('.modal-content').html(data.html_form);
					$('#error').show();
					$('#error').html(data.error);
				}
			}
		})

		return false;
	}

	var updateLike = function(){
		var el = $(this);
		$.ajax({
			url: el.attr("data-url"),
			dataType: 'json',
			type: 'get',
			data: {
				'id': el.attr('id')
			},
			success: function(data){
				if (data.is_valid){
					el.html(data.like_html)
				} else {
					$('.error').show();
				}
			}
		})

		return false;
	}

	// Upload avatar
	$(".js-avatar").on('click', '.avatar', function(){
		$('#fileupload').click();
	})

	// Profile 
	$('.body-profile').on('submit', '#js-profile-form', saveProfileForm)

	$(".js-like").click(updateLike);

})

