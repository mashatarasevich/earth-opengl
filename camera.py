import numpy as np
from matrix import rotate

class Camera:
    def __init__(self, sensivity=0.1):
        self.sens = sensivity
        self.reset()

    def reset(self):
        self.rotation = np.eye(4)
        self.add_yawpitch = np.eye(4)
        self.add_roll = np.eye(4)

    def total_rotation(self):
        return self.rotation @ self.add_yawpitch @ self.add_roll

    def set_add_rotation(self, dx, dy):
        yaw   = self.sens * dx
        pitch = self.sens * dy
        yaw_mat   = rotate(yaw  , 0, 1, 0)
        pitch_mat = rotate(pitch, 1, 0, 0)
        self.add_yawpitch = pitch_mat @ yaw_mat

    def set_add_rotation_roll(self, dx, dy):
        roll = -5 * self.sens * (dx - dy)
        roll_mat  = rotate(roll, 0, 0, 1)
        self.add_roll = roll_mat 

    def commit_rotation(self, dx, dy):
        self.set_add_rotation(dx, dy)
        self.rotation = self.rotation @ self.add_yawpitch
        self.add_yawpitch = np.eye(4)

    def commit_rotation_roll(self, dx, dy):
        self.set_add_rotation_roll(dx, dy)
        # Z @ YP @ R = Z' @ YP
        self.rotation = self.rotation @ self.add_yawpitch @ self.add_roll @ self.add_yawpitch.T
        self.add_roll = np.eye(4)
