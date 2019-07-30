$(function(){
	var loadForm = function(){
		var el = $(this);
		$.ajax({
			url: el.attr("data-url"),
			type: 'get',
			dataType: 'json',
			beforeSend: function(){
				$('#myModal').modal("show");
			},
			success: function(data){
				$('.modal-content').html(data.html_form)
			}
		})
		return false;
	}

	var saveForm = function(){
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
					location.reload();
				} else {
					$('.modal-content').html(data.html_form);
					$('#error').show();
					$('#error').html(data.error);
				}
			}
		})

		return false;
	}

	// Login
	$('.login').on('click', loadForm)
	$('.modal-content').on('submit', '#js-login-form', saveForm);

	// Register
	$('.register').click(loadForm);
	$('.modal-content').on('submit', '#js-register-form', saveForm);

})

