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

})