from paddleocr import PaddleOCR
import os
import cv2
import imp
from flask import Flask, render_template, request, session, redirect, url_for, flash
from os.path import exists

img_name = ""

def getPrescription():
	list = []
	ocr_model = PaddleOCR(lang='en')
	
	# Check if file exists
	if exists(img_name):
		result = ocr_model.ocr(img_name)
	else:
		flash("Error: File not found or camera disconnected.")
		return redirect(url_for('home'))

	for res in result:
		list.append(res[1][0])

	os.remove(img_name) 
	return list

def getPic():
	global img_name
	
	try:
		cam = cv2.VideoCapture(-1)
	except:
		return redirect(url_for('home'))
	cv2.namedWindow("Press \"spacebar\" to take a photo.")

	while True:
		ret, frame = cam.read()
		if not ret:
			break
		cv2.imshow("Press \"spacebar\" to take a photo.", frame)

		k = cv2.waitKey(1)
		if k%256 == 32:
			# SPACE pressed
			img_name = "opencv_frame_0.png"
			cv2.imwrite(img_name, frame)
			print("{} written!".format(img_name))
			break

	cam.release()
	cv2.destroyAllWindows()

