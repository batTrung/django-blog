$(function(){

	   $('#js-photo').click(function(){
        $('#fileupload').click();
        return false;
     });
     

     $("#fileupload").fileupload({
        url: $("#fileupload").attr('data-url'),
        dataType: 'json',
        done: function (e, data) {
          if (data.result.is_valid) {
            $('#photo-include').html(data.result.photo_html);
            $('.message').html('<span id="upload" style="color:#20c997;">Cập nhật thành công!</span>');
          } else {
            $('.message').html('<span id="upload" style="color:#dc3545;">Ảnh không hợp lệ!</span>');
          }
        }
      });

})