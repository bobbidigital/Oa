$(document).ready(function() {  
 
	//select all the a tag with name equal to modal
	$('input[name="modalFadeIn"]').click(function(e) {
		//Cancel the link behavior
		e.preventDefault();
     
		//Get the screen height and width
		var maskHeight = $(document).height();
		var maskWidth = $(window).width();
     
		//Set height and width to mask to fill up the whole screen
		$('#mask').css({'width':maskWidth,'height':maskHeight});
         
		//transition effect     
		$('#mask').fadeIn(1000);    
		$('#mask').fadeTo("slow",0.8);  
     
		//Get the window height and width
		var winH = $(window).height();
		var winW = $(window).width();
               
		//Set the popup window to center
		$('#dialogBox').css('top',  winH/2-$('#dialogBox').height()/2);
		$('#dialogBox').css('left', winW/2-$('#dialogBox').width()/2);
     
		//transition effect
		$('#dialogBox').fadeIn(2000); 
     
	    });
     
	//if close button is clicked
	$('.window .close').click(function (e) {
		//Cancel the link behavior
		e.preventDefault();
		$('#mask, .window').hide();
	});     
     
	//if mask is clicked
	$('#mask').click(function () {
		$(this).hide();
		$('.window').hide();
	});         
     
});

function addDropDownType(type) {

    var url = "/Management/Save/" +  type;
    var nameField = $('input[name="nameField"]').val();
    var descField = $('input[name="descField"]').val();
    if(nameField == "") {
	alert("NAME is a required field");
	return;
    }
    $.post(url, { name: nameField, desc: descField, response: "partial" },
	   function( response ) {
	       tbl = $('table[class="tablesorter"]');
	       $(tbl).append(response);
	   }
    );
}
 
