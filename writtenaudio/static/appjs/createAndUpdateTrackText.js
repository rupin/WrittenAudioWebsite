// A $( document ).ready() block.

function updateTimeMarker(trackID, timeMarker)
{
	$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
        	//console.log(getCookie('csrftoken'))
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         
     }
});
	URL='http://localhost:8000/updateTrackText/'+trackID+"/"

	requestdata='{"time_marker": '+timeMarker+""+'}'
	
	$.ajax({
	    url: URL,
	    type: 'PATCH',
	    data:requestdata,
	    contentType: "application/json",
	    dataType: "json",	    
	    success: function(result) {
	        // Do something with the result
	    }
	});
}



$( document ).ready(function() {
	
	
	 
    $('select').on('change', function() {
  			select_type=$(this).attr('data_select_type');
  			tracktextid=$(this).attr('data_id');
  			selected_value=$(this).find('option:selected').text()
  			//console.log(selected_value)
  			if(select_type=='h')
  			{
  				hourValue=selected_value
  				minuteValue=$('#m_'+tracktextid).find('option:selected').text()
  				secondsValue=$('#s_'+tracktextid).find('option:selected').text()
  			}
  			else if(select_type=='m')
  			{
  				minuteValue=selected_value
  				hourValue=$('#h_'+tracktextid).find('option:selected').text()
  				secondsValue=$('#s_'+tracktextid).find('option:selected').text()
  			}
  			else if(select_type=='s')
  			{
  				secondsValue=selected_value
  				minuteValue=$('#m_'+tracktextid).find('option:selected').text()
  				hourValue=$('#h_'+tracktextid).find('option:selected').text()
  			}
  			else
  			{
  				//console.log('Gone')
  				return
  			}
  			
  			updated_time_marker=(parseInt(hourValue)*3600)+(parseInt(minuteValue)*60)+parseInt(secondsValue)
  			updateTimeMarker(tracktextid,updated_time_marker)
	});
});