/*

UTILITIES

*/


//Computes a background color between red and green based on a 1 to 100 value passed to it
function compute_background(value){

	red    = 0;
	green  = 0;

	if (value < 50){
		red   = 255;
		green = Math.floor(2.55 * value * 2);
	}
	else{
		green = 255;
		red   = Math.floor(2.55 * (100 - value) * 2);
	}

	css_value = "rgb(" + red + ", " + green + ", 0)";
	return css_value;

};

//Computes a color between white and green based on a 1 to 100 value passed to it
function compute_background_only_green(value){

	not_green = 255 - value*2.55;
	css_value = "rgb(" + not_green + ",255," + not_green + ")";
	return css_value;

}
function compute_background_only_red(value){
	not_red = 255-value*2.55;
	css_value = "rgb(255,"+not_red+","+not_red+")"
	return css_value
}