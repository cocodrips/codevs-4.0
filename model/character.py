from codevs import *
from point import Point
import random


class Character(object):
    def __init__(self, cid, y, x, hp, type, forceType=ForceType.NEET, turn=0):
        self.cid = cid
        self.point = Point(x, y)
        self.hp = hp
        self.type = type
        self.goal = []
        self.turn = turn
        self.isFix = False
        self.group = []
        self.forceType = forceType


    def goToPoint(self, point):
        if random.random() < 0.1 * (self.cid % 10):
            if point.y - self.point.y > 0:
                return 'D'
            if point.y - self.point.y < 0:
                return 'U'
        if point.x - self.point.x > 0:
            return 'R'
        if point.x - self.point.x < 0:
            return 'L'
        if point.y - self.point.y > 0:
            return 'D'
        if point.y - self.point.y < 0:
            return 'U'
        return False


    def closest(self, field):
        pass

    def isAround(self, obj, range):
        return self.point.dist(obj) <= range