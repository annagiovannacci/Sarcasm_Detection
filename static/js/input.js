var radio_choice = 0
var example = false
var label_example = ""
function choose(sel) {
	$("#main-container").hide()
	$("#explanation-container").hide()
	$("#main-text").replaceWith("<p id = "+"main-text"+"></p>")
	$("#confidence").replaceWith("<p id = "+"confidence"+"></p>")
	$("#user-text-editable").replaceWith("<div id="+"user-text-editable"+" contenteditable="+"True"+"></div>")
	$("#user-tweet-input").replaceWith("<div id="+"user-tweet-input"+" contenteditable="+"True"+"></div>")
	$("#doc-par").replaceWith("<p id="+"doc-par"+"></p>")
	$("#tweet-text").replaceWith("<p id = "+"tweet-text"+"></p>")
	$("#tweet-confidence").replaceWith("<p id = "+"tweet-confidence"+"></p>")



	if (sel.options[sel.selectedIndex].value ==1){
		$("#tweet-container").hide();
		$("#form-text-short").hide();
		$("#form-container").show();
		$("#multilingual-choice").hide();


	}
	else if (sel.options[sel.selectedIndex].value==2){
		$("#multilingual-choice").show();
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
	$("#real_value").replaceWith("<p id ="+"real_value>");


	//Gets:
	//	the test given in input by the user
	 //Keeps the text in a global variable
	
	var text = $("#user-text-editable").text();
	console.log(text)
	input_text = text;	
	
	hash=false
	
	$.getJSON($SCRIPT_ROOT + '/prediction_long_text', {
		text: text
	}, function(data1){

		$.getJSON($SCRIPT_ROOT+'/explain_prediction',{
			text: text
		},function(data){
			$(".loader").hide();
			$("#form-text-short").show();		
			$("#main-container").show();
			$("#user-text-editable").replaceWith("<div id="+"user-text-editable"+" contenteditable="+"True"+"></div>")
		//show the prediction & the confidence
		//var span_sentence = $(document.createElement('span')).text(data1['long_text_pred']);
		text = text.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
		$("#main-text").append($(document.createElement('span')).text("Prediction: ").append("<span id="+"prediction"+">"+data1['long_text_pred']+"</span>"));
		if (data1['long_text_pred']=='REAL'){
			$("#prediction").css('background-color', compute_background_only_green(data1['confidence']))
			
		}
		if (data1['long_text_pred']=='FAKE'){			
			$("#prediction").css('background-color', compute_background_only_red(data1['confidence']))
		}
		if (data1['long_text_pred']=='SATIRICAL'){
			$("#prediction").css('background-color', compute_background_only_blue(data1['confidence']))
		}
		console.log(example)
		if (example == true){
			console.log("Show")
			$("#real_value").append($(document.createElement('span')).text("True label: ").append("<span id="+"real"+">"+label_example+"</span>"));
			if (label_example == "FAKE"){
				console.log("here")
				$("#real").css('background-color',compute_background_only_red(100))
			}
			if (label_example =='REAL'){
				$("#real").css('background-color',compute_background_only_green(100))
			}
			if (label_example =='SATIRICAL'){
				$("#real").css('background-color',compute_background_only_blue(100))
			}

		}	
		var confidence_sentence = $(document.createElement('span')).text(("Confidence: "+data1['confidence'].toString()+"%"))
		$("#confidence").append(confidence_sentence)
		example = false
		label_example =""
		//show the explanation
		
		start_word = 0
		a = 0
		text = text.replace(/ /g, "")
		console.log(text)
		text_1 = new Array()
		var dict = {}
		for (var u = 0; u < text.length; u++){
			if (text[u].match(/[^\w\s]/))
				dict[u] = text[u]
			}
		text = text.replace(/[^\w\s]/g,"")

		for (var i=0; i<data['tokenization'].length; i++){
			if (i != data['tokenization'].length-1){
				if (data['tokenization'][i+1].match(/#/g)){
				console.log("found")	
				hash = true
				}
			}
			str = data['tokenization'][i].replace(/#/g,'')
			console.log(hash)
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
			var sentence = $(document.createElement('span')).text(text_1.join('')+"");
			while(text_1.length > 0){
				text_1.pop()
			}
			$(sentence).addClass('sentence');
			if (data1['long_text_pred']=='REAL'){
				$(sentence).css('background-color', compute_background_only_green(data['explanation'][0][i]*100))
				
			}
			if (data1['long_text_pred']=='FAKE'){			
				$(sentence).css('background-color', compute_background_only_red(data['explanation'][0][i]*100))
			}
			if (data1['long_text_pred']=='SATIRICAL'){
				$(sentence).css('background-color', compute_background_only_blue(data['explanation'][0][i]*100))
			}

		$("#user-text-editable").append(sentence);	
		if (hash==false){
			console.log("NOT FOUND")
			$("#user-text-editable").append($(document.createElement('span')).text(" "))
			}
		hash = false
		}
		$("#explanation-container").show()
		$("#tweetexp").hide()
		$("#lgexp").show()
	});
	
});
});

$("#submit-tweet").click(function(){
	$("#submit-tweet").hide();
	$("#explanation-container").hide();
	$("#tweet-text-container").hide();
	$(".loader").show();

	//Gets:
	//	the test given in input by the user

	
	$("#tweet-text").replaceWith("<p id = "+"tweet-text"+"></p>")
	$("#tweet-confidence").replaceWith("<p id = "+"tweet-confidence"+"></p>")
	$("#true-tweet").replaceWith("<p id="+"true-tweet"+"></p>")
	if(document.getElementById('ml').checked){
		radio_choice = 1;
	} 
	else if (document.getElementById('sl').checked){
		radio_choice = 2;
	}
	console.log(radio_choice)
	var text = $("#user-tweet-input").text();
	console.log(text)
	input_text = text; //Keeps the text in a global variable
	hash=false
	console.log(text)
	$.getJSON($SCRIPT_ROOT + '/multilingual_tweet', {
		text: text,
		scope: radio_choice
	}, function(data){

		$.getJSON($SCRIPT_ROOT+'/explain_prediction_single_tweet',{
			text: text,
			scope: radio_choice
		},function(data1){
		$(".loader").hide();
		$("#submit-tweet").show();
		$("#tweet-text-container").show();
		$("#user-tweet-input").replaceWith("<div id="+"user-tweet-input"+" contenteditable="+"True"+"></div>")
		text = text.normalize("NFD").replace(/[\u0300-\u036f]/g, "")

		//show the prediction
		var span_sentence = $(document.createElement('span')).text("Prediction: ").append("<span id="+"tp"+">"+data['tweet_pred']+"</span>");
		$("#tweet-text").append(span_sentence);	
		if (data['tweet_pred']=="SATIRE"){
			$("#tp").css('background-color',compute_background_only_blue(data['confidence']))
		}
		else if (data['tweet_pred']=="NOT_SATIRE"){
			$("#tp").css('background-color',compute_background_only_green(data['confidence']))
		}
		else if (data['tweet_pred']=="FAKE"){
			$("#tp").css('background-color',compute_background_only_red(data['confidence']))
		}
		var confidence_sentence = $(document.createElement('span')).text(("Confidence: "+data['confidence'].toString()+"%"))
		$("#tweet-confidence").append(confidence_sentence)
		if (example == true){
			$("#true-tweet").append($(document.createElement('span')).text("True label: ").append("<span id="+"realt"+">"+label_example+"</span>"));
			if (label_example == "FAKE"){
				console.log("here")
				$("#realt").css('background-color',compute_background_only_red(100))
			}
			if (label_example =='NOT_SATIRE'){
				$("#realt").css('background-color',compute_background_only_green(100))
			}
			if (label_example =='SATIRE'){
				$("#realt").css('background-color',compute_background_only_blue(100))
			}

		}else if (example==false){
			$("#doc-par").replaceWith("<p id="+"doc-par"+"></p>")
		}
		example = false	
		label_example = ""
		start_word = 0
		a = 0
		text = text.replace(/ /g, "")
		text_1 = new Array()
		var dict = {}
		for (var u = 0; u < text.length; u++){
			if (text[u].match(/[^\w\s]/))
				dict[u] = text[u]
			}
		console.log(dict)
		text = text.replace(/[^\w\s]/g,"") 
		for (var i=0; i<data1['tokenization'].length; i++){
			if (i != data1['tokenization'].length-1){
				if (data1['tokenization'][i+1].match(/#/g)){
				console.log("found")	
				hash = true
				}
			}
			str = data1['tokenization'][i].replace(/#/g,'')
			console.log(str)
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
			$(sentence).addClass('sentence');
			if (data1['prediction']=='NOT_SATIRE'){
				$(sentence).css('background-color', compute_background_only_green(data1['explanation'][0][i]*100))
				
			}
			if (data1['prediction']=='SATIRE'){				
				$(sentence).css('background-color', compute_background_only_blue(data1['explanation'][0][i]*100))
			}
			if (data1['prediction']=='FAKE'){
				$(sentence).css('background-color', compute_background_only_red(data1['explanation'][0][i]*100))

			}
			console.log(sentence)
			$("#user-tweet-input").append(sentence);
			if (hash==false){
				console.log("NOT FOUND")
				$("#user-tweet-input").append($(document.createElement('span')).text(" "))
				}
			hash = false	
			}
		
		$("#explanation-container").show()
		$("#lgexp").show()
				
	});


});
});
$("#fake_one").click(function(){
	$("#user-text-editable").replaceWith("<div id="+"user-text-editable"+" contenteditable="+"True"+"></div>")
	$('body').css('cursor', 'wait');			
	$.getJSON($SCRIPT_ROOT + '/get_example', {
		label: 'FAKE'
	}, function(data){

		//Load example in the input area
		document.getElementById('user-text-editable').innerHTML += data['example'];
		example = true
		label_example = "FAKE"
		$('body').css('cursor', 'default');

	});

});

$("#real_one").click(function(){
	$("#user-text-editable").replaceWith("<div id="+"user-text-editable"+" contenteditable="+"True"+"></div>")
	$('body').css('cursor', 'wait');			
	$.getJSON($SCRIPT_ROOT + '/get_example', {
		label: 'REAL'
	}, function(data){

		//Load example in the input area
		document.getElementById('user-text-editable').innerHTML += data['example'];
		example = true
		label_example = "REAL"

		$('body').css('cursor', 'default');

	});

});
$("#satirical_one").click(function(){
	$("#user-text-editable").replaceWith("<div id="+"user-text-editable"+" contenteditable="+"True"+"></div>")
	$('body').css('cursor', 'wait');			
	$.getJSON($SCRIPT_ROOT + '/get_example', {
		label:'SATIRICAL'
	}, function(data){

		//Load example in the input area
		document.getElementById('user-text-editable').innerHTML += data['example'];
		example = true
		label_example = "SATIRICAL"
		$('body').css('cursor', 'default');

	});

});
$("#terrible_one").click(function(){
	$("#user-text-editable").replaceWith("<div id="+"user-text-editable"+" contenteditable="+"True"+"></div>")
	$('body').css('cursor', 'wait');			
	$.getJSON($SCRIPT_ROOT + '/get_worst_predictions', {
	}, function(data){

		//Load example in the input area
		document.getElementById('user-text-editable').innerHTML += data.example;
		example = true
		label_example = data['label']
		$('body').css('cursor', 'default');

	});

});
$("#ironic_statement").click(function(){
	$("#user-tweet-input").replaceWith("<div id="+"user-tweet-input"+" contenteditable="+"True"+"></div>")
	$("#doc-par").replaceWith("<p id="+"doc-par"+"></p>")
	$('body').css('cursor', 'wait');			
	$.getJSON($SCRIPT_ROOT + '/get_ironic_examples', {
	}, function(data){
		example = true
		label_example = "SATIRE"
		//Load example in the input area
		document.getElementById('user-tweet-input').innerHTML += data['example'];
		document.getElementById('doc-par').innerHTML+=data['doc']
		console.log(data['doc'])
		$('body').css('cursor', 'default');

	});

});
$("#tweet_ansa").click(function(){
	$("#user-tweet-input").replaceWith("<div id="+"user-tweet-input"+" contenteditable="+"True"+"></div>")
	$("#doc-par").replaceWith("<p id="+"doc-par"+"></p>")
	$('body').css('cursor', 'wait');			
	$.getJSON($SCRIPT_ROOT + '/get_example_ansa', {
	}, function(data){
		example = true
		label_example = "NOT_SATIRE"
		//Load example in the input area
		document.getElementById('user-tweet-input').innerHTML += data['example'];
		$('body').css('cursor', 'default');

	});

});