function checkResponseIsReady(trackID)
{
  $.ajaxSetup({
     beforeSend: function(xhr, settings) {
         
          xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         
     }
});
  URL=getBaseURL()+'/isTrackResultAvailable/'+trackID+"/"  
  
  $.ajax({
      url: URL,
      type: 'PATCH',
      data:'{}',
      contentType: "application/json",
      dataType: "json",     
      success: function(result) {
        if(!result.processed)
        {
          // Means the json file has not yet been generated
          //we must check again in 10 seconds
          $('#track_generation_modal').trigger("not-processed")
        }
        else
        {
              trackID=result['id']
              file_name=result['audio_file']
              showAndPlayTrack(trackID,file_name);
        }
        
      }
  });
}


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
          
          //$("#audio-modal").show()
          //enableButton(trackTextId)

          trackID=result['id']
          file_name=result['audio_file']
          showAndPlayTrack(trackID,file_name);

         
      },
      error: function (jqXHR, exception) {

        $('#track_generation_modal').trigger("timed-out")
      }
  });

}

function showAndPlayTrack(trackID, file_name)
{

          //audioURL=result['file_url']
          //audioURL=audioURL+"?a="+Math.random()
          URL=getDownloadFileURL(trackID) // Inside common.js
          //console.log(URL)
          $('#combined_track_audio').append("<source id='sound_src' src=" + URL + " type='audio/mpeg'>");
          $("#combined_track_audio").trigger('load').trigger('play');
          $("#waiting_div").hide();
          $("#track_audio_container").show();
          $("#track_file_name_div").show()
          $("#file_name_tag").html(file_name)

}

$(document).ready(function(){
    $("#downloadbutton").on('click', function(){

       track_id==$(this).attr("data-track_id")
       downloadTrackFile(track_id);

    })

    

    $('#showmodalForCombine').on('click', function(){

        $('#track_generation_modal').show();

        track_id=$(this).attr('data_track_id');
        generateCombinedAudio(track_id)
    })


    $('#track_generation_modal').on('timed-out', function(){

       track_id=$(this).attr('data_track_id');
        setTimeout(function(track_id){
          checkResponseIsReady(track_id)
        }, 10000, track_id);

      

    });

    $('#track_generation_modal').on('not-processed', function(){
        track_id=$(this).attr('data_track_id');

        setTimeout(function(track_id){
          checkResponseIsReady(track_id)
        }, 10000, track_id);
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

   

})