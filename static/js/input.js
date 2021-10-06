function choose(sel) {
	$("#main-container").hide()
	$("#explanation-container").hide()
	$("#main-text").replaceWith("<p id = "+"main-text"+"></p>")
	$("#confidence").replaceWith("<p id = "+"confidence"+"></p>")
	$("#user-text-editable").replaceWith("<div id="+"user-text-editable"+" contenteditable="+"True"+"></div>")
	$("#user-tweet-input").replaceWith("<div id="+"user-tweet-input"+" contenteditable="+"True"+"></div>")



	if (sel.options[sel.selectedIndex].value ==1){
		$("#welcome-container").hide();
		$("#tweet-container").hide();
		$("#form-text-short").hide();
		$("#form-container").show();

	}
	else if (sel.options[sel.selectedIndex].value==2){
		$("#welcome-container").hide();
		$("#form-container").hide();
		$("#tweet-container").show();
		$("#form-text-short").show();

		

		
	}		



};


//Submits the form with the input text given by the user
$("#submit-text").click(function(){

	//Shows loading animation
	$(".loader").show();		
	$("#explanation-container").hide();
	$("#main-container").hide();

	$("#main-text").replaceWith("<p id = "+"main-text"+"></p>")
	$("#confidence").replaceWith("<p id = "+"confidence"+"></p>")

	//Gets:
	//	the test given in input by the user
	 //Keeps the text in a global variable
	
	var text = $("#user-text-editable").text();
	console.log(text)
	input_text = text;	
	$("#user-text-editable").replaceWith("<div id="+"user-text-editable"+" contenteditable="+"True"+"></div>")

	
	$.getJSON($SCRIPT_ROOT + '/prediction_long_text', {
		text: text
	}, function(data1){

		$.getJSON($SCRIPT_ROOT+'/explain_prediction',{
			text: text
		},function(data){
			$(".loader").hide();
			$("#form-text-short").show();		
			$("#main-container").show();
		
		//show the prediction & the confindence
		var span_sentence = $(document.createElement('span')).text(data1['long_text_pred']);
		$(span_sentence).addClass('sentence');
		$("#main-text").append(span_sentence);	
		var confidence_sentence = $(document.createElement('span')).text((data1['confidence'].toString()))
		$(confidence_sentence).addClass('sentence');
		console.log(data['confidence'])
		$("#confidence").append(confidence_sentence)
		$("#confidence").append($(document.createElement('span')).text("% "))
		
		//show the explanation
		
		start_word = 0
		a = 0
		text = text.replace(/ /g, "")
		text_1 = new Array()
		var dict = {}
		for (var u = 0; u < text.length; u++){
			if (text[u].match(/[^\w\s]/))
				dict[u] = text[u]
			}
		text = text.replace(/[^\w\s]/g,"")
		for (var i=0; i<data['tokenization'].length; i++){
			str = data['tokenization'][i].replace(/#/g,'')
			str = str.replace(/ /g, '')
			end_word = start_word + str.length;
			
			for (k=start_word; k<end_word; k++){
				text_1.push(text[k])
				for (var key in dict){
					if (k+1+a == key){
						text_1.splice(key,0,dict[key])
						a = a + 1
					}
				}	
			}
			start_word = end_word
			console.log(text_1)
			var sentence = $(document.createElement('span')).text(text_1.join('')+" ");
			while(text_1.length > 0){
				text_1.pop()
			}
			console.log(data['tokenization'][i])
			console.log(data['prediction'])
			$(sentence).addClass('sentence');
			if (data1['long_text_pred']=='REAL'){
				$(sentence).css('background-color', compute_background_only_green(data['explanation'][0][i]*100))
				
			}
			if (data1['long_text_pred']=='FAKE'){			
				console.log(data['explanation'][0][i]*100)	
				console.log(compute_background_only_blue(data['explanation'][0][i]*100))
				$(sentence).css('background-color', compute_background_only_blue(data['explanation'][0][i]*100))
			}
			if (data1['long_text_pred']=='SATIRICAL'){
				$(sentence).css('background-color', compute_background_only_red(data['explanation'][0][i]*100))
			}
			console.log(sentence)

		$("#user-text-editable").append(sentence);	
		$("#user-text-editable").append($(document.createElement('span')).text(" "))
		};
		$("#explanation-container").show()
		$("#tweetexp").hide()
		$("#lgexp").show()
	});
	
});
});

$("#submit-tweet").click(function(){
	$("#submit-tweet").hide();
	$("#explanation-container").hide();
	$("#main-container").hide();
	$(".loader").show();

	//Gets:
	//	the test given in input by the user

	
	$("#main-text").replaceWith("<p id = "+"main-text"+"></p>")
	$("#confidence").replaceWith("<p id = "+"confidence"+"></p>")
	
	var text = $("#user-tweet-input").text();
	console.log(text)
	input_text = text; //Keeps the text in a global variable
	$("#user-tweet-input").replaceWith("<div id="+"user-tweet-input"+" contenteditable="+"True"+"></div>")
	console.log(text)
	$.getJSON($SCRIPT_ROOT + '/multilingual_tweet', {
		text: text
	}, function(data){

		$.getJSON($SCRIPT_ROOT+'/explain_prediction_single_tweet',{
			text: text
		},function(data1){
		//Hides the input textarea and shows the results
		//$("#tweet-container").hide();
		$(".loader").hide();
		$("#submit-tweet").show();
		$("#main-container").show();

		//show the prediction
		var span_sentence = $(document.createElement('span')).text(data['tweet_pred']);
		$(span_sentence).addClass('sentence');
		$("#main-text").append(span_sentence);	
		var confidence_sentence = $(document.createElement('span')).text((data['confidence'].toString()))
		$(confidence_sentence).addClass('sentence');
		console.log(data['confidence'])
		$("#main-text").append(span_sentence);
		$("#confidence").append(confidence_sentence)
		$("#confidence").append($(document.createElement('span')).text("% "))

		start_word = 0
		a = 0
		text = text.replace(/ /g, "")
		text_1 = new Array()
		var dict = {}
		for (var u = 0; u < text.length; u++){
			if (text[u].match(/[^\w\s]/))
				dict[u] = text[u]
			}
		text = text.replace(/[^\w\s]/g,"")
		for (var i=0; i<data1['tokenization'].length; i++){
			str = data1['tokenization'][i].replace(/#/g,'')
			str = str.replace(/ /, '')
			end_word = start_word + str.length;
			
			for (k=start_word; k<end_word; k++){
				text_1.push(text[k])
				for (var key in dict){
					if (k+1+a == key){
						text_1.splice(key,0,dict[key])
						a = a + 1
					}
				}	
			}
			start_word = end_word
			console.log(text_1)
			var sentence = $(document.createElement('span')).text(text_1.join('')+"");
			while(text_1.length > 0){
				text_1.pop()
			}
			console.log(data1['tokenization'][i])
			console.log(data1['prediction'])
			$(sentence).addClass('sentence');
			if (data1['prediction']=='NOT_SATIRE'){
				console.log(data1['explanation'][0][i])
				$(sentence).css('background-color', compute_background_only_green(data1['explanation'][0][i]*100))
				
			}
			if (data1['prediction']=='SATIRE'){				
				$(sentence).css('background-color', compute_background_only_red(data1['explanation'][0][i]*100))
			}
			console.log(sentence)
			$("#user-tweet-input").append(sentence);	
			$("#user-tweet-input").append($(document.createElement('span')).text(" "))
		
			}
		

		$("#explanation-container").show()
		$("#lgexp").hide()
		$("#tweetexp").show()
				
	});


});
});
$("#examples li").click(function(){
	$("#user-tweet-input").replaceWith("<div id="+"user-tweet-input"+" contenteditable="+"True"+"></div>")
	var filename = $(this).attr('name');
	console.log(filename)
	$('body').css('cursor', 'wait');			
	$.getJSON($SCRIPT_ROOT + '/get_example', {
		example: filename
	}, function(data){

		//Load example in the input area
		document.getElementById('user-text-editable').innerHTML += data['example'];

		$('body').css('cursor', 'default');

	});

});

