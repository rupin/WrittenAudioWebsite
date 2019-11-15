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

function getDownloadFileURL(trackID)
{
  
  return getBaseURL()+'/downloadTrack/'+trackID+"/?a="+Math.random() 
}

function toHHMMSS(secondsNumber) {
    var sec_num = parseInt(secondsNumber, 10); // don't forget the second param
    var hours   = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    var seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (hours   < 10 && hours > 0) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    return hours + ':' + minutes + ':' + seconds;
}
