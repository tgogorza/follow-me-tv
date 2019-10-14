from imutils.video import VideoStream
from imutils.video import FPS
# import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import os
from time import sleep
import numpy as np

VIDEO_STREAM = 'http://192.168.0.30:8000/stream.mjpg'
# FLIP_VIDEO = False
PROCESS_HEIGHT = 480
PROCESS_WIDTH = 640
INPUT_HEIGHT = 480
INPUT_WIDTH = 640

curr_path = os.path.dirname(os.path.realpath(__file__))

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
detector = cv2.CascadeClassifier(os.path.join(curr_path, '../data/haarcascade_frontalface_alt.xml'))
 
# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
# vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
vs = cv2.VideoCapture(VIDEO_STREAM)

def convert_coords(box):
	x1 = int(INPUT_WIDTH * box[3] / PROCESS_WIDTH)
	y1 = int(INPUT_HEIGHT * box[0] / PROCESS_HEIGHT)
	x2 = int(INPUT_WIDTH * box[1] / PROCESS_WIDTH)
	y2 = int(INPUT_HEIGHT * box[2] / PROCESS_HEIGHT)
	return (x1, y1, x2, y2)

# loop over stream
while True:
	ret, frame = vs.read()
	# if FLIP_VIDEO:
	# 	frame = cv2.flip(frame, 0)

	# convert to grayscale and resize for face detections
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	gray = imutils.resize(gray, width=PROCESS_WIDTH)
 
	# detect faces in the grayscale frame
	rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
	#rects=[]
	# Get boxes coordinates
	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
	# Translate boxes coords to original frame size
	boxes = [convert_coords(box) for box in boxes]
	# Draw bounding boxes
	[cv2.rectangle(frame,(box[0], box[1]),(box[2], box[3]),(0,255,0),2) for box in boxes]
	
	# Get the horizontal center for each bounding box
	centers = [box[0] + ((box[2] - box[0]) / 2) for box in boxes]
	if centers:
		centroid = np.mean(centers)
		cv2.line(frame, (int(centroid), 0), (int(centroid), INPUT_HEIGHT), (0,0,200), 2)

	# Show frame
	cv2.imshow('Stream IP Camera OpenCV',frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	# sleep(1)

vs.release()
cv2.destroyAllWindows()

