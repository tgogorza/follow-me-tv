from rotator import Rotator
import time
import requests
from flask import request
from envs.config import rotation_step
from stream.config import INPUT_WIDTH, INPUT_HEIGHT
from camera import PiCam

SERVER_URL = "http://192.168.0.47:5000/action"

rotator = Rotator()
cam = PiCam(INPUT_WIDTH, INPUT_HEIGHT)

def get_action(frame):
    data = frame.tostring()
    response = requests.post(SERVER_URL, data=data).json()
    return response['action']

def get_rotation(curr_angle, action):
    if action == '1':
        step = rotation_step
    elif action == '2':
        step = -rotation_step
    else:
        step = 0
    new_angle = curr_angle + step
    return new_angle

while True:
    frame = cam.get_image()
    action = get_action(frame)
    curr_angle = rotator.getAngle()
    new_angle = get_rotation(curr_angle, action)
    if new_angle != curr_angle:
        rotator.setAngle(new_angle)
    time.sleep(0.5)

