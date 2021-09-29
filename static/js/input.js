/*

HANDLES INPUT FROM THE USER IN THE INITAL FORM
*/

function choose(sel) {
	$("#main-container").hide()
	$("#explanation-container").hide()
	$("#main-text").replaceWith("<p id = "+"main-text"+"></p>")
	$("#text-pred").replaceWith("<p id = "+"text-pred"+"></p>")

	if (sel.options[sel.selectedIndex].value ==1){
		$("#welcome-container").hide();
		$("#tweet-container").hide();
		$("#form-container").show();

	}
	else if (sel.options[sel.selectedIndex].value==2){
		$("#welcome-container").hide();
		$("#form-container").hide();
		$("#tweet-container").show();
	}		



};


//Submits the form with the input text given by the user
$("#submit-text").click(function(){

	//Shows loading animation
	$(".loader").show();		
	$("#explanation-container").hide();
	$("#main-container").hide();

	$("#main-text").replaceWith("<p id = "+"main-text"+"></p>")
	$("#text-pred").replaceWith("<p id = "+"text-pred"+"></p>")


	//Gets:
	//	the test given in input by the user
	var text = $("#user-text-input").val();
	input_text = text; //Keeps the text in a global variable
	

	$.getJSON($SCRIPT_ROOT + '/prediction_long_text', {
		text: text
	}, function(data1){

		//Hides the input textarea and shows the results
		
	

		$.getJSON($SCRIPT_ROOT+'/explain_prediction',{
			text: text
		},function(data){
			$(".loader").hide();
			//document.getElementById("user-text-input").value= ""
			$(".loader").hide();
			$("#form-container").show();		
			$("#user-text-input").show();
			$("#main-container").show();
		
		//show the prediction
			var span_sentence = $(document.createElement('span')).text(data1['long_text_pred']);
			$(span_sentence).addClass('sentence');
			$("#main-text").append(span_sentence);
			$("#user-text-input").append(text)
			$("#explanation-container").show();
			$("#text-pred").val("")
			for (var i=0; i<data['tokenization'].length; i++){
				for (var j = 0; j < data['tokenization'][i].length; j++){
				var span_element = $(document.createElement('span')).text(data['tokenization'][i][j]+" ");
				//console.log(data['tokenization'][i][j])
				$(span_element).addClass('sentence');
				if (data['prediction'][i]=='NOT_SATIRE'){
					$(span_element).css('background-color', compute_background_only_green(data['explanation'][i][0][j]*100))
					
				}
				if (data['prediction'][i]=='SATIRE'){				
					$(span_element).css('background-color', compute_background_only_red(data['explanation'][i][0][j]*100))
				}
				//document.getElementById("user-text-input").value= document.getElementById("user-text-input").value + $(span_element).text()
				$("#text-pred").append(span_element);	
				$("#text-pred").append($(document.createElement('span')).text(" "))
				//$("#user-text-input").append($(document.createElement('span')).text(" "))
				}
			}

		});
	});
});

$("#submit-tweet").click(function(){
	$("#submit-tweet").hide();
	$(".loader").show();

	//Gets:
	//	the test given in input by the user
	
	var text = $("#user-tweet-input").val();
	input_text = text; //Keeps the text in a global variable
			
	$.getJSON($SCRIPT_ROOT + '/multilingual_tweet', {
		text: text
	}, function(data){

		//Hides the input textarea and shows the results
		//$("#tweet-container").hide();
		$(".loader").hide();
		$("#submit-tweet").show();
		$("#main-container").show();
		
		

			//show the prediction
		var span_sentence = $(document.createElement('span')).text(data['tweet_pred']);
		$(span_sentence).addClass('sentence');
		$("#main-text").append(span_sentence);	
				
	});


});

