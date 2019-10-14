import cv2
from stream import config
import imutils
import os
import numpy as np

curr_path = os.path.dirname(os.path.realpath(__file__))

class FaceDetector:
    def __init__(self):
        print("[INFO] loading encodings + face detector...")
        self.detector = cv2.CascadeClassifier(os.path.join(curr_path, '../data/haarcascade_frontalface_alt.xml'))

    def get_faces(self, frame):
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        # convert to grayscale and resize for face detections
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = imutils.resize(gray, width=config.PROCESS_WIDTH)
    
        # detect faces in the grayscale frame
        rects = self.detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        # Get boxes coordinates
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
        # Translate boxes coords to original frame size
        boxes = [self.convert_coords(box) for box in boxes]
        return boxes
        
    def get_centroid(self, boxes):
        # Get the horizontal center for each bounding box
        centers = [box[0] + ((box[2] - box[0]) / 2) for box in boxes]
        centroid = np.mean(centers)
        return centroid    

    def convert_coords(self, box):
        x1 = int(config.INPUT_WIDTH * box[3] / config.PROCESS_WIDTH)
        y1 = int(config.INPUT_HEIGHT * box[0] / config.PROCESS_HEIGHT)
        x2 = int(config.INPUT_WIDTH * box[1] / config.PROCESS_WIDTH)
        y2 = int(config.INPUT_HEIGHT * box[2] / config.PROCESS_HEIGHT)
        return (x1, y1, x2, y2)