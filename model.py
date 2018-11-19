import numpy as np
from matrix import rotate

class Rotatable:
    def __init__(self, sensivity=0.1):
        self.sens = sensivity
        self.reset()

    def reset(self):
        self.rotation = rotate(-90, -1, 0, 0) @ rotate(240, 0, -1, 0)
        self.add_rotation = np.eye(4)

    def total_rotation(self):
        return self.rotation @ self.add_rotation

    def set_add_rotation(self, dx, dy):
        sens = self.sens
        self.add_rotation = rotate(sens * dy, -1, 0, 0) @ rotate(sens * dx, 0, -1, 0)

    def commit_rotation(self, dx, dy):
        self.set_add_rotation(dx, dy)
        self.rotation = self.rotation @ self.add_rotation
        self.add_rotation = np.eye(4)


class Model(Rotatable):
    def __init__(self, pts, tri):
        super().__init__(sensivity = 0.1)
        x = pts[:, 0:1]
        y = pts[:, 1:2]
        z = pts[:, 2:3]
        # SP (0, 0, -1) - lat = -90 deg, NP (0, 0, 1) - lat = 90 deg
        lat = np.arcsin(z) / (np.pi / 2)
        lon = np.arctan2(y + x, x - y) / np.pi
        self.vertices = np.hstack((pts, lon, lat))
        self.triangles = tri
