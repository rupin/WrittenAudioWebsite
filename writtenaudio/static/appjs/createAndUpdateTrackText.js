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

function getBaseURL()
{
  var getUrl = window.location;
  var baseUrl = getUrl.protocol + "//" + getUrl.host 
  return baseUrl;
}

/**********************************************************/

function updateTrackText(trackID, trackTextData)
{
	$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         
        	xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         
     }
});
	URL=getBaseURL()+'/updateTrackText/'+trackID+"/"	
	
	$.ajax({
	    url: URL,
	    type: 'PATCH',
	    data:trackTextData,
	    contentType: "application/json",
	    dataType: "json",	    
	    success: function(result) {
	        // Do something with the result
         if(result.mark_for_deletion) // flag that says if this track is processed
         {
            track_text_id=result.id
            $("#row_"+track_text_id).remove()
         }
        
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
  URL=getBaseURL()+'/updateTrack/'+trackID+"/"  
  
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

function updateVoiceProfile(trackID, trackData)
{
    $.ajaxSetup({
       beforeSend: function(xhr, settings) {
           
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
           
       }
  });
    URL=getBaseURL()+'/updateVoiceProfile/'+trackID+"/"  
    
    $.ajax({
        url: URL,
        type: 'PATCH',
        data:trackData,
        contentType: "application/json",
        dataType: "json",     
        success: function(result) {
            //$('#track_title_text_input').trigger('track_title_saved');
            //console.log(result)
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
	URL=getBaseURL()+'/CreateTrackEmptyRow/'+trackid	
	
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

function generateCombinedAudio(track_id)
{

  $.ajaxSetup({
     beforeSend: function(xhr, settings) {
         
          xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         
     }
});
  URL=getBaseURL()+'/CombinedAudioTrack/'+track_id+"/"  
  
  $.ajax({
      url: URL,
      type: 'PATCH',        
      success: function(result) {
          trackID=result['id']
          //audioURL=result['file_url']
          //audioURL=audioURL+"?a="+Math.random()
          URL=getBaseURL()+'/downloadTrack/'+trackID+"/" 
          $('#combined_track_audio').append("<source id='sound_src' src=" + URL + " type='audio/mpeg'>");
          $("#combined_track_audio").trigger('load').trigger('play');
          $("#waiting_div").hide();
          $("#track_audio_container").show();
          $("#track_file_name_div").show()
          $("#file_name_tag").html(result['audio_file'])
          //$("#audio-modal").show()
          //enableButton(trackTextId)
         
      }
  });

}

/**********************************************************/


function text_clean_up(newtext)
{
	newtext = newtext.replace(/(\r\n|\n|\r)/gm, ""); //Remove all Line breaks
  newtext = newtext.replace(/</gm, "");
  newtext = newtext.replace(/>/gm, "");
  newtext=  newtext.trim()

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
  requestdata='{"mark_for_deletion":"True"}'
  updateTrackText(trackTextId,requestdata)
	
}
/**********************************************************/
function generateAudio(trackTextId)
{
  $.ajaxSetup({
     beforeSend: function(xhr, settings) {
         
          xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         
     }
});
  URL=getBaseURL()+'/generateAudio/'+trackTextId+"/"  
  
  $.ajax({
      url: URL,
      type: 'PATCH',        
      success: function(result) {

          object_id=result.id
          $("#duration_container_"+object_id).html(result.duration)
          //console.log(result)
          URL=getBaseURL()+'/downloadTrackText/'+object_id+"/" 
          //console.log(audioURL)
          audioURL=URL+"?a="+Math.random()    
          //var audio = new Audio(audioURL);
          //audio.play();
          var count = $("#track_audio").children().length;
          //console.log(count)
          $('#track_audio').empty()
          var count = $("#track_audio").children().length;
          //console.log(count)
          
          $('#track_audio').append("<source id='sound_src' src=" + audioURL + " type='audio/mpeg'>");
          $("#track_audio").trigger('load').trigger('play');
         
          $("#audio-modal").show()
          enableButton(trackTextId)
         
          
          
      }
  });
}

function play(tracktextid)
{
  disableButton(tracktextid);
  generateAudio(tracktextid);
  //URL="https://storage.cloud.google.com/written-audio-files/"+tracktextid+".mp3?a="+Math.random()
  //$("#audio-source").attr('src', URL);
  //$('#audio-modal').show();
  //console.log(URL)

  

}

function disableButton(tracktextid)
{
  buttonRef=$("#play_button_"+tracktextid)
  //console.log(buttonRef.attr('data-id'))
  $(buttonRef).addClass("disabled")
}

function enableButton(tracktextid)
{
  
  buttonRef=$("#play_button_"+tracktextid)
  //console.log(buttonRef.attr('data-id'))
  $(buttonRef).removeClass("disabled")
}

function downloadTrackFile(trackID)
{
  
  URL=getBaseURL()+'/download/'+trackID+"/"  
  
  window.location.assign(URL);


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
          //disableButton(tracktextid);

  				requestdata='{"processed":"False","voice_profile": '+selected_value+""+'}'
  				
  			}
        else
        {
          return
        }
  			
  			
  			updateTrackText(tracktextid,requestdata)
	});

    $(this).trigger("disable_audio_button")


    
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
          if(textValue!="")
          {
              requestdata='{"processed":"False","text": "'+textValue+'"}'
              //console.log(requestdata)
              //disableButton(tracktextid);
              updateTrackText(tracktextid,requestdata)
        }
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

  $('#track_generation_modal').show();

  track_id=$(this).attr('data_track_id');
  generateCombinedAudio(track_id)
})




$('#combine_audio_close_modal').on('click', function(event){
  target_modal=$(this).attr("data-dismiss")
  //console.log(target_modal)
  if(target_modal)
  {
    $("#"+target_modal).hide();
  }
  //$("#combined_track_audio").pause();
  $("#combined_track_audio").trigger('pause');
  $("#track_audio_container").hide();
  $("#waiting_div").show();
  $("#track_file_name_div").hide()
  //$(event).stopPropagation()

});

$(document).on('keypress change focusout',"input[type=text][data-input-type=time_marker]", function(){
  //console.log("I am here")
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



$(document).keydown(function(event) {
//console.log(event) 
  if (event.keyCode == 27) { 
   $("#audio-modal").hide()
  }
});

$("#downloadbutton").on('click', function(){

   track_id==$(this).attr("data-track_id")
   downloadTrackFile(track_id);

})

$("select[data_select_type=track_voice_profile]").on("change", function(){
        trackid=$(this).attr('data_id');
        selected_value=$(this).find('option:selected').val() 
        requestdata='{"voice_profile":' +selected_value+'}'
        updateVoiceProfile(trackid,requestdata)     

})






});







