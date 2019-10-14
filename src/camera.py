import os
import numpy as np

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
        return self.centroid

    def rotate(self, direction):
        self.centroid += 1 if direction == "left" else -1
        # Boundary check
        self.centroid = min(max(self.centroid, 0), self.image_width-1)


class PiCam:
    def __init__(self, width=640, height=480):
        try:
            from picamera import PiCamera
            from picamera.array import PiRGBArray
        except:
            print('Not running on RaspberryPi')
        self.camera = PiCamera()
        self.camera.resolution = (width, height)
        self.camera.framerate = 24
        
    def get_image(self):
        frame = PiRGBArray(self.camera)
        self.camera.capture(frame, 'rgb')
        return frame.array