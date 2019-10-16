// A $( document ).ready() block.

function updateTimeMarker(trackID, timeMarker)
{

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