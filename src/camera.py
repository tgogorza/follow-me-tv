import numpy as np
from keras.utils import to_categorical

# class Camera:
#     def __init__(self, image_width):
#         self.image_width = image_width

#     def get_image(self):
#         raise NotImplementedError()

#     def rotate(self):
#         raise NotImplementedError()


class FakeCamera:
    def __init__(self, image_width, centroid = None):
        # super(FakeCamera, self).__init__(image_width)
        self.image_width = image_width
        if centroid is None:
            self.centroid =  int(np.random.uniform(image_width))
        else:
            self.centroid = centroid

    def get_image(self):
        image = "|" + "|".join(["   " if slot != self.centroid else " + " for slot in range(self.image_width)]) + "|\n"
        return image

    def get_centroid(self):
        centroid_onehot = to_categorical(self.centroid, self.image_width)
        return centroid_onehot, self.centroid

    def rotate(self, direction):
        self.centroid += 1 if direction == "left" else -1
        # Boundary check
        self.centroid = min(max(self.centroid, 0), self.image_width-1)


# class PiCamera(Camera):
#     def __init__(self, image_width):
#         super.__init__(self, image_width)
#         # pass

#     def get_image(self):
#         pass