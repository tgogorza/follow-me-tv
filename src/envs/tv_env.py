"""
Based on the OpenAI Gym cartpole environment
"""

import math
import gym
import time
import sys
from contextlib import closing
from six import StringIO
from gym import spaces, logger
from gym.utils import seeding
import numpy as np
# from rotator import Rotator
from camera import FakeCamera
import envs.config as config
from .spaces import OneHot


class TVEnv(gym.Env):
    """
    Description:
        The TV is attached to an articulated wall mount. The articulation is controlled by a servo motor attached which will rotate to foolow a person. The input feed is a standard RBG video feed.

    Observation: 
        Type: Box(4)
        Num	Observation                 Min         Max
        0	TV Angle                    0           180
        1	Centroid Distance           -Inf        Inf
        
    Actions:
        Type: Discrete(3)
        Num	Action
        0	Do nothing
        1	Increase angle by 10 deg
        2   Decrease angle by 10 deg
        
    Reward:
        Reward is determined by the mean distance of all subjects in the picture to the horizontal center of the picture. Essentially, we want the TV to face to the horizontal centroid of people in the room.

    Starting State:
        TV facing center (at angle 90) [35..145]

    Episode Termination:
        TV Angle is more than 145 or less than 35 degrees
        Episode length is greater than 50
        Considered solved when the average reward is greater than or equal to X over 50 consecutive trials.
    """
    
    metadata = {
        'render.modes': ['human', 'ansi'],
        'video.frames_per_second' : 2
    }

    def __init__(self):
        # Angles at which to fail the episode
        # self.rotator = Rotator(config.lower_bound, config.upper_bound)
        self.rotation_step = config.rotation_step

        self.num_slots = config.num_slots
        # self.image_width = config.image_width
        self.center_slot = int(self.num_slots / 2)
        # self.slot_width = self.image_width / self.num_slots

        # self.angle = self.rotator.getAngle()
        self.episode_length = 50

        self.camera = FakeCamera(self.num_slots)

        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Discrete(self.num_slots)

        self.seed()
        self.viewer = None
        self.state = None

        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))

        self.execute_action(action)
        new_centroid_slot = self.camera.get_centroid()

        if new_centroid_slot == self.center_slot:
            self.steps_at_center += 1
        else:
            self.steps_at_center = 0

        reward = self.get_reward(new_centroid_slot) 
        done = self.steps >= self.episode_length

        if not done:
            self.steps += 1
            
        self.state = new_centroid_slot
        return new_centroid_slot, reward, done, {}


    def reset(self):
        self.camera = FakeCamera(self.num_slots)
        self.state = self.camera.get_centroid()
        self.steps = 0
        self.steps_at_center = 0
        # self.angle = 90
        # return np.array(self.state)
        return self.state

    def render(self, mode='human'):
        outfile = StringIO() if mode == 'ansi' else sys.stdout

        out = self.camera.get_image()
        outfile.write(out)
        
        # No need to return anything for human
        if mode != 'human':
            with closing(outfile):
                return outfile.getvalue()

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None

    def execute_action(self, action):
        if action == 1:
            self.camera.rotate("left")
            # self.rotator.setAngle(self.rotator.getAngle() + self.rotation_step)
        elif action == 2:
            self.camera.rotate("right")
            # self.rotator.setAngle(self.rotator.getAngle() - self.rotation_step)

    def get_reward(self, slot):
        '''
        Reward gets determine by the inverse of distance.
        If angle remains unchanges, reward gets increased.

        '''
        if slot == self.center_slot:
            distance_reward = self.steps_at_center * 5000.0
            # Future enhancement: Once it finds a center position, favor that position (so it doesn't move all the time)
        else:
            slot_distance = np.abs(slot - self.center_slot)
            distance_reward = -1000.0 * slot_distance #100.0 / (2**slot_distance)

        # distance_reward = 100 * (1 / distance)
        # angle_reward = (20 - (abs(new_angle - old_angle)))
        # return distance_reward + angle_reward
        return distance_reward
