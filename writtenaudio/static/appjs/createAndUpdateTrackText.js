// A $( document ).ready() block.
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

function updateTrackText(trackID, trackTextData)
{
	$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         
        	xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         
     }
});
	URL='http://localhost:8000/updateTrackText/'+trackID+"/"	
	
	$.ajax({
	    url: URL,
	    type: 'PATCH',
	    data:trackTextData,
	    contentType: "application/json",
	    dataType: "json",	    
	    success: function(result) {
	        // Do something with the result
	    }
	});
}

function updateTrack(trackID, trackData)
{
  $.ajaxSetup({
     beforeSend: function(xhr, settings) {
         
          xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         
     }
});
  URL='http://localhost:8000/updateTrack/'+trackID+"/"  
  
  $.ajax({
      url: URL,
      type: 'PATCH',
      data:trackData,
      contentType: "application/json",
      dataType: "json",     
      success: function(result) {
          // Do something with the result
      }
  });
}

function AddRowToTable(trackid)
{
	$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         
        	xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         
     }
});
	URL='http://localhost:8000/CreateTrackEmptyRow/'+trackid	
	
	$.ajax({
	    url: URL,
	    type: 'GET',
	      
	    success: function(result) {
	        console.log(result)
	        $("#track_text_tbody").append(result)
	    }
	});
}


function text_clean_up(newtext)
{
	newtext = newtext.replace(/(\r\n|\n|\r)/gm, ""); //Remove all Line breaks

	return newtext
}

function deleteTrackText(trackTextId)
{
	$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         
        	xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         
     }
});
	URL='http://localhost:8000/deleteTrackText/'+trackTextId	
	
	$.ajax({
	    url: URL,
	    type: 'GET',	      
	    success: function(result) {
	        track_text_id=result
	        $('#row_'+track_text_id).remove()
	        
	    }
	});
}




$( document ).ready(function() {
	
	
	 
    $(document).on('change', 'select', function() {
  			select_type=$(this).attr('data_select_type');
  			tracktextid=$(this).attr('data_id');
  			selected_value=$(this).find('option:selected').val()
  			//console.log(selected_value)
  			if(select_type=='h')
  			{
  				hourValue=selected_value
  				minuteValue=$('#m_'+tracktextid).find('option:selected').text()
  				secondsValue=$('#s_'+tracktextid).find('option:selected').text()
          updated_time_marker=(parseInt(hourValue)*3600)+(parseInt(minuteValue)*60)+parseInt(secondsValue)
          requestdata='{"time_marker": '+updated_time_marker+""+'}'
  			}
  			else if(select_type=='m')
  			{
  				minuteValue=selected_value
  				hourValue=$('#h_'+tracktextid).find('option:selected').text()
  				secondsValue=$('#s_'+tracktextid).find('option:selected').text()
          updated_time_marker=(parseInt(hourValue)*3600)+(parseInt(minuteValue)*60)+parseInt(secondsValue)
          requestdata='{"time_marker": '+updated_time_marker+""+'}'
  			}
  			else if(select_type=='s')
  			{
  				secondsValue=selected_value
  				minuteValue=$('#m_'+tracktextid).find('option:selected').text()
  				hourValue=$('#h_'+tracktextid).find('option:selected').text()
          updated_time_marker=(parseInt(hourValue)*3600)+(parseInt(minuteValue)*60)+parseInt(secondsValue)
          requestdata='{"time_marker": '+updated_time_marker+""+'}'
  			}
  			else if(select_type=='voice_profile')
  			{
  				requestdata='{"processed":"False","voice_profile": '+selected_value+""+'}'
  				
  			}
        else
        {
          return
        }
  			
  			
  			updateTrackText(tracktextid,requestdata)
	});


    
    var timeoutId;

$(document).on('keypress change focusout', 'textarea', function () {
    

    // If a timer was already started, clear it.
    if (timeoutId) clearTimeout(timeoutId);
    a=50
    that=$(this);
    // Set timer that will save comment when it fires.
    timeoutId = setTimeout(function (textareaRef) {
        // Make ajax call to save data.
        	tracktextid=$(textareaRef).attr('data_id');
        	textValue=$(textareaRef).val()
        	textValue=text_clean_up(textValue)
        	requestdata='{"processed":"False","text": "'+textValue+'"}'
        	//console.log(requestdata)
  			updateTrackText(tracktextid,requestdata)
    }, 750, that);
});

$("#addnewrow").on('click', function(){
	trackid=$(this).attr('data_track_id')
	AddRowToTable(trackid)


});

$("#tracktitle").on('keypress change focusout', function () {
    

    // If a timer was already started, clear it.
    if (timeoutId) clearTimeout(timeoutId);
    
    that=$(this);
    // Set timer that will save comment when it fires.
    timeoutId = setTimeout(function (titleRef) {
        // Make ajax call to save data.
          trackid=$(titleRef).attr('data_id');
          textValue=$(titleRef).val()
          textValue=text_clean_up(textValue)
          requestdata='{"title": "'+textValue+'"}'
          //console.log(requestdata)
        updateTrack(trackid,requestdata)
    }, 750, that);
});






});