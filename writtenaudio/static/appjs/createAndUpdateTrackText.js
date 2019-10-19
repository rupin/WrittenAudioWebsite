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

/**********************************************************/

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

/**********************************************************/

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
          $('#track_title_text_input').trigger('track_title_saved');
      }
  });
}

/**********************************************************/

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
	        //console.log(result)
	        $("#track_text_tbody").append(result)
	    }
	});
}

/**********************************************************/


function text_clean_up(newtext)
{
	newtext = newtext.replace(/(\r\n|\n|\r)/gm, ""); //Remove all Line breaks
  newtext = newtext.replace(/</gm, "");
  newtext = newtext.replace(/>/gm, "");

	return newtext
}

/**********************************************************/

function calculateDuration(inputValue)
{
  if(isNaN(inputValue))
  {
    //Means probably user has entered in hh:mm:ss format. Returns isNaN if no numeric input is put
     calculatedTime=inputValue.split(':').reduce((acc,time) => (60 * acc) + +time);
     //console.log(calculatedTime)
     if(isNaN(calculatedTime))
     {
      throw "Invalid Input"
     }
     else
     {
        return Math.trunc(calculatedTime)
     }
 
    


  }
  else
  {
    // User has entered seconds directly
    return Math.trunc(inputValue)
  }
}

/**********************************************************/

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
/**********************************************************/
function generateAudio(trackTextId)
{
  $.ajaxSetup({
     beforeSend: function(xhr, settings) {
         
          xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         
     }
});
  URL='http://localhost:8000/generateAudio/'+trackTextId+"/"  
  
  $.ajax({
      url: URL,
      type: 'PATCH',        
      success: function(result) {
          //track_text_id=result
          //$('#row_'+track_text_id).remove()
          
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

// $("#track_title_text_input").on('keypress change focusout', function () {
    

//     // If a timer was already started, clear it.
//     if (timeoutId) clearTimeout(timeoutId);
    
//     that=$(this);
//     // Set timer that will save comment when it fires.
//     timeoutId = setTimeout(function (titleRef) {
//         // Make ajax call to save data.
//           trackid=$(titleRef).attr('data_id');
//           textValue=$(titleRef).val()
//           textValue=text_clean_up(textValue)
//           requestdata='{"title": "'+textValue+'"}'
//           //console.log(requestdata)
//         updateTrack(trackid,requestdata)
//     }, 1000, that);
// });

$("#save_title_button").on('click', function () {
    

   
      // Make ajax call to save data.
      $(this).removeClass('btn-primary').addClass('btn-disabled');
      titleInput=$("#track_title_text_input")
      trackid=$(titleInput).attr('data_id');
      textValue=$(titleInput).val()
      textValue=text_clean_up(textValue)
      requestdata='{"title": "'+textValue+'"}'
      //console.log(requestdata)
      updateTrack(trackid,requestdata)
    
});


$('#page_title_span').on('click', function(){

  $(this).hide();
  $("#input_group").show()
})

$('#track_title_text_input').on('track_title_saved', function(){
  
  $("#input_group").hide()
  $("#save_title_button").addClass('btn-primary').removeClass('btn-disabled');
  updated_title_value=text_clean_up($(this).val())
  $("#page_title_span").html(updated_title_value).show()
  $(this).val(updated_title_value)
})

//

$('#showmodal').on('click', function(){

  $('#track_settings_modal').show();
})


$('.close').on('click', function(event){
  target_modal=$(this).attr("data-dismiss")
  //console.log(target_modal)
  if(target_modal)
  {
    $("#"+target_modal).hide();
  }
  //$(event).stopPropagation()

});

$("input[type=text][data-input-type=time_marker]").on('keypress change focusout', function(){

  // If a timer was already started, clear it.
    if (timeoutId) clearTimeout(timeoutId);
    
    that=$(this);
    // Set timer that will save comment when it fires.
    timeoutId = setTimeout(function (inputRef) {
        // Make ajax call to save data.
          tracktextid=$(inputRef).attr('data_id');
          textValue=$(inputRef).val()
          textValue=text_clean_up(textValue)
          try
          {
            trackDuration=calculateDuration(textValue)
            $(inputRef).css("background-color", "#FFFFFF"); 
            requestdata='{"time_marker": "'+trackDuration+'"}'          
            updateTrackText(tracktextid,requestdata)
          }
          catch(err)
          {
            $(inputRef).css("background-color", "red");            
          }
          
    }, 750, that);

});






});