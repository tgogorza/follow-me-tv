import os
import numpy as np
from keras.utils import to_categorical
from stream import config
import cv2
import imutils

curr_path = os.path.dirname(os.path.realpath(__file__))

# class Camera:
#     def __init__(self, image_width):
#         self.image_width = image_width

#     def get_image(self):
#         raise NotImplementedError()

#     def rotate(self):
#         raise NotImplementedError()


class FakeCamera:
    "FakeCamera used for RL agent training. Just returns a centroid on a virtual slot and moves the centroid with right/left rotations"
    def __init__(self, image_width, centroid = None):
        # super(FakeCamera, self).__init__(image_width)
        self.image_width = image_width
        if centroid is None:
            self.centroid =  int(np.random.uniform(image_width))
        else:
            self.centroid = centroid

    def get_image(self):
        image = "|" + "|".join(["   " if slot != self.centroid else " + " for slot in range(self.image_width)]) + "|\n"
        return image

    def get_centroid(self):
        centroid_onehot = to_categorical(self.centroid, self.image_width)
        return centroid_onehot, self.centroid

    def rotate(self, direction):
        self.centroid += 1 if direction == "left" else -1
        # Boundary check
        self.centroid = min(max(self.centroid, 0), self.image_width-1)


class PiCamera:
    def __init__(self, url, image_width):
        # super.__init__(self, image_width)
        self.stream_url = url
        print("[INFO] starting video stream...")
        self.video_stream = cv2.VideoCapture(self.stream_url)
        print("[INFO] loading encodings + face detector...")
        self.detector = cv2.CascadeClassifier(os.path.join(curr_path, '../data/haarcascade_frontalface_alt.xml'))

    def get_image(self):
        ret, frame = self.video_stream.read()
        if config.FLIP_VIDEO:
            frame = cv2.flip(frame, 0)
        return frame

    def get_faces(self, frame):
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