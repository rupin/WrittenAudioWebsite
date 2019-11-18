
$(document).ready(function(){
$("#translate_track_modal_close").on('click', function(){

	modal_id=$(this).attr("data-dismiss")
	$("#"+modal_id).hide();
})

$('#translatebutton').on("click", function()
{
	translation_language_id=$("#translation_dropdown").find('option:selected').val();
	trackID=$(this).attr("data-track_id");
	requestdata='{"language": "'+translation_language_id+'"}'
	sendTranslationRequest(trackID,requestdata);

});

	
});

function openTranslateModal(trackID)
{
	$("#translate_track_modal").show();
	$('#translatebutton').attr("data-track_id", trackID);
}

function sendTranslationRequest(trackID, requestData)
{
	$.ajaxSetup({
     beforeSend: function(xhr, settings) {
         
        	xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         
     }
});
	URL=getBaseURL()+'/translateTrack/'+trackID+"/"	
	
	$.ajax({
	    url: URL,
	    type: 'PATCH',
	    data:requestData,
	    contentType: "application/json",
	    dataType: "json",	    
	    success: function(result) {
	    	clonedTrackID=result.id
	    	window.location.href = '/editTrack/'+clonedTrackID; //relative to domain
	    
        
	    }
	});

}