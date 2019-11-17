
$(document).ready(function(){
$("#translate_track_modal_close").on('click', function(){

	modal_id=$(this).attr("data-dismiss")
	$("#"+modal_id).hide();
})

	
})

function openTranslateModal(trackID)
{
	$("#translate_track_modal").show();
	$('#translatebutton').attr("data-track_id", trackID);
}