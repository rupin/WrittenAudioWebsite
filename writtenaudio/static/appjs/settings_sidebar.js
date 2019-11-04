 $(document).ready(function(){

 $("#settings_sidebar_icon").click(function () {
    if (!$(this).hasClass("open"))
     {
      $(this).animate({"right": "250px"});
      $("#settings_sidebar").animate({"right": "0"});
      $(this).addClass("open");

    } 
    else
     {
      $(this).animate({"right": "0"});
      $("#settings_sidebar").animate({"right": "-250px"});
      $(this).removeClass("open");
    }
  });

 $("#save_track_param").on("click", function(){
        trackid=$(this).attr('data_id');
        voice_profile_dropdown=$("#voice_profile_"+trackid);
        audio_speed_slider=$("#audio_speed_"+trackid);
        audio_pitch_slider=$("#audio_pitch_"+trackid);
        selected_voice_profile=$(voice_profile_dropdown).find('option:selected').val()
        audio_speed=$(audio_speed_slider).val() 
        audio_pitch=$(audio_pitch_slider).val() 
        requestdata='{"audio_pitch":'+audio_pitch+',"audio_speed":'+audio_speed+', "voice_profile":' +selected_voice_profile+'}'
        updateVoiceProfile(trackid,requestdata)     

})

 $("input[type='range']").on('input change', function(){

    data_output_element=$(this).attr("data-output-element")
    $("#"+data_output_element).val($(this).val())

  //$("#current_audio_speed").val($(this).val()+"x")
 })






})

 function updateVoiceProfile(trackID, trackData)
{
    $.ajaxSetup({
       beforeSend: function(xhr, settings) {
           //getCookie function define din common.js
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
            $("#settings_sidebar_icon").trigger('click')
        }
    });
}