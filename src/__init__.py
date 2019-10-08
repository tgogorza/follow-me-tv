from gym.envs.registration import register

register(
    id='follow-me-tv-v0',
    entry_point='follow_me_tv.envs:TVEnv',
)