/*

HANDLES INPUT FROM THE USER IN THE INITAL FORM
*/
$("#long_text_analyzer").click(function(){
	$("#welcome-container").hide();
	$("#first-choice").hide();
	$("#form-container").show();

});
$("#tweet_analyzer").click(function(){
	$("#welcome-container").hide();
	$("#first-choice").hide();
	$("#tweet-container").show();

})

//Submits the form with the input text given by the user
$("#submit-text").click(function(){

	//Shows loading animation
	$("#submit-text").hide();
	$(".loader").show();

	//Gets:
	//	the test given in input by the user
	var text = $("#user-text-input").val();
	input_text = text; //Keeps the text in a global variable
			
	$.getJSON($SCRIPT_ROOT + '/prediction_long_text', {
		text: text
	}, function(data){

		//Hides the input textarea and shows the results
		$("#form-container").hide();
		$(".loader").hide();
		$("#show_ex").hide();
		$("#main-container").show();
		
		

			//show the prediction
		var span_sentence = $(document.createElement('span')).text(data['long_text_pred']);
		$(span_sentence).addClass('sentence');
		$("#main-text").append(span_sentence);
		if (data['long_text_pred']== 'SATIRICAL' || data['long_text_pred']=='FAKE'){
			$("#show_ex").show();
		}
		else{
			$("#show_ex").hide()
		}	
				
	});

});
$("#ask_for_explanation").click(function(){
	var text = $("#user-text-input").val();
	input_text = text; //Keeps the text in a global variable
	$(".loader").show();
	$.getJSON($SCRIPT_ROOT+'/explain_prediction',{
		text: text
	},function(data){
		$(".loader").hide();
		$("#welcome-container").hide();
		$("#main-container").hide();
		$("#show_ex").hide()
		$("#explanation-container").show();
		for (var i=0; i<data['tokenization'].length; i++){
			for (var j = 0; j < data['tokenization'][i].length; j++){
			var span_element = $(document.createElement('span')).text(data['tokenization'][i][j]+" ");
			console.log(i);
			//console.log(data['tokenization'][i][j])
			console.log(data['explanation'][i][0][j])
			$(span_element).addClass('sentence');
			if (data['prediction'][i]=='NOT_SATIRE'){
				$(span_element).css('background-color', compute_background_only_green(data['explanation'][i][0][j]*100))
			}
			if (data['prediction'][i]=='SATIRE'){				
				console.log(data['prediction'][i])			
				$(span_element).css('background-color', compute_background_only_red(data['explanation'][i][0][j]*100))
			}
			
			$("#text-pred").append(span_element);	
			$("#text-pred").append($(document.createElement('span')).text(" "))
			}
		}
	
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
		$("#show_ex").hide();
		$("#main-container").show();
		
		

			//show the prediction
		var span_sentence = $(document.createElement('span')).text(data['tweet_pred']);
		$(span_sentence).addClass('sentence');
		$("#main-text").append(span_sentence);	
				
	});


});

