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


	// Upload avatar
	$(".js-avatar").on('click', '.avatar', function(){
		$('#fileupload').click();
	})

	// Profile 
	$('.body-profile').on('submit', '#js-profile-form', saveProfileForm)

})

