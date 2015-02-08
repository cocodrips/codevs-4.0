# -*- coding: utf-8 -*-
from codevs import *


class Resource(object):
    """
    資源クラス
    mother: この資源を守る担当の攻撃ユニット
    """
    def __init__(self, point):
        self.workers = []
        self.planners = []
        self.point = point
        self.mother = []

    def __eq__(self, other):
        return self.point == other.point

    def __repr__(self):
        return "({},{})".format(self.point.x, self.point.y)

    def reset(self):
        self.workers = []
        self.planners = []

    @property
    def volunteer(self):
        """
        実際に働いている人と、働く予定の人
        """
        return self.workers + self.planners