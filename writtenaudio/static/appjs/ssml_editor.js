$( document ).ready(function() {

$(document).on('mousedown', "button[data-button-type='emphasize']", function(){
  data_id=$(this).attr("data_id")
  //console.log(getSelectedText())
  text_area=$("textarea[data_id='"+data_id+"']")
  startOfSelection=$(text_area)[0].selectionStart
  endOfSelection=$(text_area)[0].selectionEnd

  if(startOfSelection>-1 && endOfSelection>startOfSelection)
  {
    text=$(text_area).val()
    selectedText=text.substring(startOfSelection,endOfSelection)
    pre=text.substring(0,startOfSelection)
    post=text.substring(endOfSelection)
    changedText=pre+"<emphasis>"+selectedText+"</emphasis>"+post
    $(text_area).val(changedText)
  }

  //console.log(selectedText)
})    

})