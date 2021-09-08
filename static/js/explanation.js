/*

Adds a button "Show why" that explains why a certain prediction was made
Takes:
 - text_to_explain
 - predictor
 - container: where to place the explanation
Returns:
 - HTML with explanation

*/
function add_show_why(container, predictor_name, text){
	
	var button = $(document.createElement('span')).text('Show how sentences contributed to the prediction.');
	button.attr('predictor', predictor_name);
	button.attr('text_to_explain', text);
	button.addClass('show_why');
	$(container).append(button);
	$(container).append($(document.createElement('span')).text(" "));
	
};

//Sends info to the server and shows the prediction
$(document).on('click', '.show_why', function(){

	var button = $(this);
	var container = $(this).parent().parent();

	//Send predictor's name and text to explain
	$.getJSON($SCRIPT_ROOT + '/prediction_long_text', {
		'text': $(this).attr('text_to_explain')
	}, function(data){

		//Remove 'show why' button and insert a short intro on how the explanation works
		button.empty();
		container.append($(document.createElement('p')).html("Words <span style='background-color: rgb(0,255,0)'>highlighted in green</span> support the prediction, those in <span style='background-color: rgb(255,0,0)'>red</span> counter it").css('margin', '0.5em'));
		
		//Show the explanation		
		var explanation = $(document.createElement('p')).addClass('explanation-text').html(data.explanation);
		container.append(explanation);
	});
	
	button.removeClass('show_why');
});

//Remove the [sep] token from an explanation
function remove_sep(explanation){

	var explanation_span = $(explanation).children();
	for (var i=0; i<explanation_span.length; i++){
	    if ($(explanation_span[i]).text() == "] "){
	        $(explanation_span[i]).empty();
	        break;
	    }
    	$(explanation_span[i]).empty();
	}
}
