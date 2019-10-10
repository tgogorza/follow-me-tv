import numpy as np
import tensorflow as tf
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input
from keras.optimizers import Adam
# from keras import backend as K
# from keras.utils import to_categorical

from rl.agents.dqn import DQNAgent
from rl.agents.cem import CEMAgent
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy, BoltzmannQPolicy
from rl.memory import SequentialMemory, EpisodeParameterMemory
from rl.callbacks import FileLogger, ModelIntervalCheckpoint

import envs.spaces as spaces

class FollowAgent:

    def __init__(self, env, state_size=1, num_actions=3):
        self.env_name = 'follow-me-tv-v0'
        # Get the environment and extract the number of actions.
        self.env = env
        self.num_steps = 100000 
        self.graph = None
        self.memory = SequentialMemory(limit=10000, window_length=1)
        self.policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.3, value_test=.05, nb_steps=self.num_steps)
        self.model = self.build_model(state_size, num_actions)
        self.agent = DQNAgent(model=self.model, nb_actions=num_actions, memory=self.memory, nb_steps_warmup=1000, target_model_update=1e-2, policy=self.policy)

    def build_model(self, state_size, num_actions):
        # input = Input(shape=(state_size,))
        # # onehot = K.one_hot(K.cast(input, 'uint8'), num_classes=9)
        # # x = Flatten()(onehot)
        # x = Dense(16, activation='relu')(x)
        # # x = Dense(36, activation='relu')(x)
        # # x = Dense(16, activation='relu')(x)
        # output = Dense(num_actions, activation='linear')(x)
        # model = Model(inputs=input, outputs=output)

        model = Sequential()
        model.add(spaces.OneHot(9,1))
        model.add(Flatten())
        # model.add(Dense(48, input_shape=(1,), activation='relu'))
        model.add(Dense(48, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(num_actions, activation='linear'))

        print(model.summary())
        return model

    def build_callbacks(self, env_name):
        checkpoint_weights_filename = 'dqn_' + env_name + '_weights_{step}.h5f'
        log_filename = 'dqn_{}_log.json'.format(env_name)
        callbacks = [ModelIntervalCheckpoint(checkpoint_weights_filename, interval=25000)]
        callbacks += [FileLogger(log_filename, interval=1000)]
        return callbacks

    def train(self):
        callbacks = self.build_callbacks(self.env_name)
        self.agent.compile(Adam(lr=1e-3), metrics=['mae'])
        self.agent.fit(self.env, nb_steps=self.num_steps, visualize=False, verbose=2, callbacks=callbacks)

    def test(self):
        # self.agent.compile(Adam(lr=1e-3), metrics=['mae'])
        self.agent.test(self.env, nb_episodes=25, visualize=True)

    def start_service(self, saved_model):
        self.model.load_weights(saved_model)
        self.graph = tf.get_default_graph()
        print("Loaded model from disk")

    def get_action(self, slot):
        # self.model.load_weights("/home/tomas/Projects/follow-me-tv/src/dqn_follow-me-tv-v0_weights_100000.h5f")
        # self.model.compile(Adam(lr=1e-3), metrics=['mae'])
        with self.graph.as_default():
            action = np.argmax(self.model.predict([slot]))
        return action
        
        