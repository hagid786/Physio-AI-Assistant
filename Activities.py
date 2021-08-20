"""Whassup trash"""

import numpy as np
import PoseModule as pm


class activities:
    def __init__(self, pose, angle1,angle2,angle3,angle4,angle5,angle6):
        self.pose = pose
        self.angle1 = angle1
        self.angle2 = angle2
        self.angle3 = angle3
        self.angle4 = angle4
        self.angle5 = angle5
        self.angle6 = angle6



    def flex(self):
        per1 = np.interp(self.angle1, (30, 160), (0, 100))
        per2 = np.interp(self.angle2, (30, 160), (0, 100))
        avg = (per1+per2)/2

        return avg


    def standing_crunch(self):
        pass