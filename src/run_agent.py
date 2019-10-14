import numpy as np
import gym
from gym.envs.registration import registry, register, make, spec
from envs.tv_env import TVEnv

from agent import FollowAgent
from detector import FaceDetector
from stream import config as stream_config
from envs import config as env_config
from flask import Flask, jsonify, request
# import cv2
# from PIL import Image

ENV_NAME = 'tv_env-v0'

app = Flask(__name__)

register(
    id='tv_env-v0',
    entry_point='envs.tv_env:TVEnv',
    max_episode_steps=50,
    reward_threshold=100000.0,
)

# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)
np.random.seed(3210)
env.seed(3210)
# nb_actions = env.action_space.n

slot_width = stream_config.INPUT_WIDTH / env_config.num_slots 

# cam = PiCamera(stream_config.VIDEO_STREAM, stream_config.INPUT_WIDTH)
detector = FaceDetector()
agent = FollowAgent(env) 
agent.start_service("/home/tomas/Projects/follow-me-tv/src/dqn_follow-me-tv-v0_weights_100000.h5f")

@app.route('/action', methods=['POST'])
def get_action():
    img = np.fromstring(request.data, np.uint8).reshape(stream_config.INPUT_HEIGHT, stream_config.INPUT_WIDTH, 3)
    faces = detector.get_faces(img)
    if faces:
        centroid = detector.get_centroid(faces)
        slot = int(centroid / slot_width)
        action = agent.get_action(slot)
        print("Next Action: {}".format(action))

        # [cv2.rectangle(img,(box[0], box[1]),(box[2], box[3]),(0,255,0),2) for box in faces]
        # cv2.line(img, (int(centroid), 0), (int(centroid), stream_config.INPUT_HEIGHT), (0,0,200), 2)
    else:
        action = 0
        centroid = 0
        slot = 0

    # im = Image.fromarray(img).show()

    response = {"action": str(action),
                "action_str": agent.action_str[action],
                "faces": faces,
                "centroid": str(centroid),
                "slot": str(slot),
                }

    print('{} - {} ({})'.format(response['slot'], response['action_str'], response['action']))
    return jsonify(response)


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, use_reloader=False)