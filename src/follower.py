from rotator import Rotator
import time
import requests
from envs.config import rotation_step

SERVER_URL = "http://192.168.0.47:5000/action"

rotator = Rotator()

def get_action():
    response = requests.get(SERVER_URL).json()
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
    action = get_action()
    curr_angle = rotator.getAngle()
    new_angle = get_rotation(curr_angle, action)
    if new_angle != curr_angle:
        rotator.setAngle(new_angle)
    time.sleep(0.5)

