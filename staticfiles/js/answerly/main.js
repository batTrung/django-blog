$(function(){
  var num =$(".action[style!='background-color:#f3f3f3']").length;
  $('#count-msg').text(num);

  $("#js-notifier").on('click','.action',function(){
        var $action = $(this);

        $.ajax({
          url: $action.attr("data-href"),
          dataType: 'json',
          type:'get',
          success: function(data){
            $('#js-notifier').html(data.notifiers);

          }
        })
    });


	var endpoint = ''
  var loc = window.location
  var wsStart = 'ws://'
  if (loc.protocol == 'https:'){
    wsStart = 'wss://'
  }
  endpoint = wsStart+ loc.host+'/notifier/'
  console.log(endpoint)

  var socket =  new ReconnectingWebSocket(endpoint)

  socket.onmessage = function(e){
    console.log("message",e)
    var nfData = JSON.parse(e.data)
    $('#show-notifier').prepend(nfData.text)
    $('#count-msg').text(parseInt($('#count-msg').text())+1)

  }

  socket.onopen = function(e){
    console.log("open",e);
    var data ={
    	'message': "OPEN"
    }
    socket.send(JSON.stringify(data));

  }

  socket.onerror = function(e){
    console.log("error",e)
  }
  socket.onclose = function(e){
    console.log("close",e)
  }

});	