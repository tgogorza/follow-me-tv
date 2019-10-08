# import gym
# import numpy as np

# class OneHot(gym.Space):
#     """
#     {0,...,1,...,0}

#     Example usage:
#     self.observation_space = OneHotEncoding(size=4)
#     """
#     def __init__(self, size=None):
#         assert isinstance(size, int) and size > 0
#         self.size = size
#         gym.Space.__init__(self, (), np.int64)

#     def sample(self):
#         one_hot_vector = np.zeros(self.size)
#         one_hot_vector[np.random.randint(self.size)] = 1
#         return one_hot_vector

#     def contains(self, x):
#         if isinstance(x, (list, tuple, np.ndarray)):
#             number_of_zeros = list(x).contains(0)
#             number_of_ones = list(x).contains(1)
#             return (number_of_zeros == (self.size - 1)) and (number_of_ones == 1)
#         else:
#             return False

#     def __repr__(self):
#         return "OneHotEncoding(%d)" % self.size

#     def __eq__(self, other):
#         return self.size == other.size


from keras.layers import Lambda
# We will use `one_hot` as implemented by one of the backends
from keras import backend as K

def OneHot(input_dim=None, input_length=None):
    # Check if inputs were supplied correctly
    if input_dim is None or input_length is None:
        raise TypeError("input_dim or input_length is not set")

    # Helper method (not inlined for clarity)
    def _one_hot(x, num_classes):
        return K.one_hot(K.cast(x, 'uint8'), num_classes=num_classes)

    # Final layer representation as a Lambda layer
    return Lambda(_one_hot,
                  arguments={'num_classes': input_dim},
                  input_shape=(input_length,))