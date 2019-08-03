$(document).ready(function(){

      $(".js-toggle").click(function(){

          // var selected = $('select').val();
          // var url = $('select').attr("data-url");
          $(this).toggleClass("btn-warning");

      });


      $("#js_category").add(".js-toggle").on("click",function(){
          var selected = $("#js_category").val();
          var url = $("select").attr("data-url");
          var qtop = $("#js-top").hasClass("btn-warning");
          var qnew = $("#js-new").hasClass("btn-warning");
          var data= new Object;

          data.qtop = qtop?1:0;
          data.qnew = qnew?1:0;
          data.qtype = selected;
          data.page = 1;
    

          $.ajax({
              url: url,
              type: 'get',
              data:data,
              dataType:'json',
              success: function(data){
                $('tbody').html(data.html_question_list);
                
              }
          });
      });

      var loadForm = function(){
        $.ajax({
            url : $(this).attr('data-href'),
            type: 'get',
            dataType: 'json',
            success: function(data){
              $('#question_form_include').html(data.html_form);
            }
        });
      };

      var saveForm = function(){
          var form = $(this);

          $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: 'post',
            success: function(data){
              if (data.form_is_valid) {
                  $('tbody').html(data.html_quetion_list);
                  $('#question_form_include #close_form').click();

              } else {
                $('#question_form_include').html(data.html_form);
              }
            }
          });
          return false;
      };

      $('#create_question').click(loadForm);
      $('#modalRegisterForm').on("submit","#form-question", saveForm);
      $('#modalRegisterForm').on("change","input", function(){
          var title = $(this);
          $.ajax({
            url: title.attr("data-url"),
            dataType: "json",
            data: {
              'title': title.val(),
            },
            type:'get',
            success: function(data){
              if (data.errors) {
                $('.errors').html('<span id="upload" style="color:#dc3545;">Câu hỏi này đã được hỏi. Xem tại '+data.link+' </span>');
              } else {
                $('.errors').html('');
              }
            }
          })

      });


  });