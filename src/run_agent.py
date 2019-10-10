import numpy as np
import gym
from gym.envs.registration import registry, register, make, spec
from envs.tv_env import TVEnv

from agent import FollowAgent
from camera import PiCamera
from stream import config as stream_config
from envs import config as env_config
from flask import Flask, jsonify

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

cam = PiCamera(stream_config.VIDEO_STREAM, stream_config.INPUT_WIDTH)

agent = FollowAgent(env) 
agent.start_service("/home/tomas/Projects/follow-me-tv/src/dqn_follow-me-tv-v0_weights_100000.h5f")

@app.route('/action', methods=['GET'])
def get_action():
    img = cam.get_image()
    faces = cam.get_faces(img)
    if faces:
        centroid = cam.get_centroid(faces)
        slot = int(centroid / slot_width)
        action = agent.get_action(slot)
        print("Next Action: {}".format(action))
    else:
        action = 0
        centroid = 0
        slot = 0

    
    response = {"action": str(action),
                "faces": faces,
                "centroid": str(centroid),
                "slot": str(slot),
                }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)