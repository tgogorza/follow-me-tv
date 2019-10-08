import numpy as np
import gym
from gym.envs.registration import registry, register, make, spec
from envs.tv_env import TVEnv

from agent import FollowAgent

ENV_NAME = 'tv_env-v0'

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

agent = FollowAgent(env) 

agent.train()

agent.test()