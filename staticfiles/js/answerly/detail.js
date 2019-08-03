$(function(){
	
  $('img').not('.rounded-circle').addClass("img-fluid");

	var loadForm = function(){
        $.ajax({
            url : $(this).attr('data-href'),
            type: 'get',
            dataType: 'json',
            success: function(data){
              $('#comment_form_include').html(data.html_form);
            },

        });
      };

       var saveForm = function(){
          var form = $(this);
          console.log("OKE");
          $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: 'post',
            success: function(data){
              if (data.form_is_valid) {
              	  console.log("SUCCESS");
                  $('#comments').html(data.html_comment_list);
                  $('#comment_form_include #close_form').click();

              } else {
                $('#comment_form_include').html(data.html_form);
              }
            }
          });
          return false;
      };

	$('#create_comment').click(loadForm);
	$('#modalCommentForm').on("submit","#form-comment", saveForm);

	$('#modalCommentForm').on('click','#js-cancel',function(){
		$('#comment_form_include #close_form').click();
	});


  var $up = $('#js-vote-question-up');
  var $down = $('#js-vote-question-down');
  var $cu = $('.comment_up');
  var $cd = $('.comment_down');

  var loadVote = function(){
    data= new Object;
    var $el = $(this);
    data.action = $el.attr('value');

    $.ajax({
            url : $el.attr('data-href'),
            type: 'get',  
            data: data,
            dataType: 'json',
            success: function(data){
              if (data.errors){
                
              } else{
                $el.children('span').text(data.val);
                
              }
            },

        });

    };

  $up.click(loadVote);
  $down.click(loadVote);
  $('#comments').on("click",".comment_up",loadVote);
  $('#comments').on("click",".comment_down",loadVote);

  
});