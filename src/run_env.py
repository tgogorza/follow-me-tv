import gym
from gym.envs.registration import registry, register, make, spec
from envs.tv_env import TVEnv

register(
    id='tv_env-v0',
    entry_point='envs.tv_env:TVEnv',
    max_episode_steps=50,
    reward_threshold=250.0,
)

env = gym.make('tv_env-v0')

for i_episode in range(20):
    observation = env.reset()
    for t in range(50):
        env.render()
        print(observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)        
        if done:
            print("Episode finished after {} timesteps with reward {}".format(t+1, reward))
            break
env.close()