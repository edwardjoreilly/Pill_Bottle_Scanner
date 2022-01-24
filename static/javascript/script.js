//Global variables
var passwordErrorBool = false;
var mySubmitButton;

//Functions NEED TO MODIFY PASSWORD CHECKER TO CHECK IF BOTH PASSWORDS ARE THE SAME
function checkPassword(x) {
	var passwordDiv = document.getElementById("passwordError");
	var upper = false;
	var lower = false;
	var number = false;

	//Loops for every character in the string "x" and the if, else if, and else statements check if the character is an upper or lower case letter or a number.
	for (var n = 0; n < x.length; n++) {
		 var character = x.charCodeAt(n);

		if((character > 47 && character < 58)) {
			number = true;
		}

		else if((character > 64 && character < 91)) {
			upper = true;
		}

		else if((character > 96 && character < 123)) {
			lower = true;
		}
	}

	//This if statement and else statement check if at least one upper-case letter, one lower-case letter, and a number are found. If this is the case, then no errors occur and the passwordErrorBool flag will be false and the div will be invisible.
	if(upper == true && lower == true && number == true) {
		passwordDiv.setAttribute("class", "invisible");
		passwordErrorBool = false;
	}

	else {
		passwordDiv.setAttribute("class", "visible");
		passwordErrorBool = true;
	}
} //End checkPassword

function buttonClick() {
	var password = document.getElementById("passwordField").value;
	var successDiv = document.getElementById("success");

	//Checks the password for errors, sets passwordErrorBool to true if an error is found.
	checkPassword(password);

	//If any of the error flags are true this sets the background color to red.
	if(passwordErrorBool == true) {
		successDiv.setAttribute("class", "invisible");
		document.body.style.background = "red";
	}

	//If no errors are found, then the user was successful and the background color remains unchanged or is returned back to white.
	else {
		successDiv.setAttribute("class", "visible");
		document.body.style.background = "white";
	}
} //End buttonClick

function start() {
	mySubmitButton = document.getElementById("submitButton");

	//Event triggered if the submit button is clicked and the buttonClick function is initialized.
	mySubmitButton.addEventListener("click", buttonClick);
} //End start

//Initiates start function when window is loaded.
window.addEventListener("load", start);
