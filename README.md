#New Additions
Facial Recognition

must install cv2 and face_recognition

#register.html
added another 'file' form field to upload a front facing image to use for facial login

#login.html
added a link to login using facial recognition -> facelogin.html

#facelogin.html
asks user for their username
upon button press submission, camera takes a photo and then compares to the saved photo in the database
added a link to login using password -> login.html

#app.py
import cv2
import face_recognition

## users table
added another column to store the face image filename

## facelogin
attempted to make similar to login
only takes in the username and then uses the username to retrieve the filename for the saved face image
gets the saved image from the uploads folder and then uses that to compare to the taken photo during login
when user submits a photo is taken, this is then compared to the saved photo via face_recognition
if face is not detected in photo an error is thrown, otherwise it checks to see if the faces match
if faces match login happens just like the login page, otherwise flashes login failed try again with password
if no matching username flashes account doesn't exist

## register
added faceimagename to submit a file and upload the filename to the database
attempted to error check the file similar to uploads
uploads the data to the database


#End


# Webcam Easy JS
This is a javascript library for accessing webcam stream and taking photos.

You can easily add it as a module to your own app.

- Streaming webcam on desktop computer or mobile
- Switch back or front cameras on mobile
- Take pictures and be able to download.

## Live Demo
**[https://bensonruan.com/how-to-access-webcam-and-take-photo-with-javascript/](https://bensonruan.com/how-to-access-webcam-and-take-photo-with-javascript/)**

![webcam-easy-demo](https://bensonruan.com/wp-content/uploads/2020/04/webcam-easy-demo-ok.gif)

## Installation

#### Use Git Clone
``` shell
git https://github.com/bensonruan/webcam-easy.git
```

#### OR Use NPM
[![NPM](https://nodei.co/npm/webcam-easy.png?compact=true)](https://nodei.co/npm/webcam-easy/)
``` shell
npm install webcam-easy
```

## Usage

#### 1. Include script tag in html <head>
```html
<script type="text/javascript" src="https://unpkg.com/webcam-easy/dist/webcam-easy.min.js"></script>
```
    or Import into javascript
``` js
import Webcam from 'webcam-easy';
```


#### 2. Place elements in HTML
```html
<video id="webcam" autoplay playsinline width="640" height="480"></video>
<canvas id="canvas" class="d-none"></canvas>
<audio id="snapSound" src="audio/snap.wav" preload = "auto"></audio>
```

#### 3. Call constructor in javascript
``` js
const webcamElement = document.getElementById('webcam');
const canvasElement = document.getElementById('canvas');
const snapSoundElement = document.getElementById('snapSound');
const webcam = new Webcam(webcamElement, 'user', canvasElement, snapSoundElement);
```

#### 4. Start Webcam 
``` js
webcam.start()
   .then(result =>{
      console.log("webcam started");
   })
   .catch(err => {
       console.log(err);
   });
```

#### 5. Take Photo
``` js
var picture = webcam.snap();
``` 

#### 6. Stop Webcam 
``` js
webcam.stop();
```

## Functions
- start(startStream) : start streaming webcam 
  - get permission from user
  - get all video input devices info
  - select camera based on facingMode 
  - start stream
  
  startStream is optional parameter, default value is true
      
- stop() : stop streaming webcam
  
- stream() : start streaming webcam to video element
  
- snap() : take photo from webcam
  
- flip() : change Facing mode and selected camera

## Properties

- facingMode : 'user' or 'enviroment'
- webcamList : all available camera device
- webcamCount : number of available camera device
