function seePassword() {
	var x = document.getElementById("password");
			
	if (x.type === "password") {
		x.type = "text";
	}

	else {
		x.type = "password";
	}
}

function seePassword2() {
	var x = document.getElementById("password2");
			
	if (x.type === "password") {
		x.type = "text";
	}

	else {
		x.type = "password";
	}
}










// Get the modal
var modal = document.getElementById("myModal");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var images = document.getElementsByClassName("images");
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");

for(var i = 0; i < images.length; i++) {
	var img = images[i];

	img.onclick = function(evt){
		console.log(evt);
		modal.style.display = "block";
		modalImg.src = this.src;
		captionText.innerHTML = this.alt;
	}
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}
