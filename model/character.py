# -*- coding: utf-8 -*-
from codevs import *
from point import Point
import random


class Character(object):
    """
    全てのユニットのクラス
    """
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
        self.rightRate = 0.2 * (self.cid % 10)
        self.mother = []

    def goToPoint(self, point):
        if random.random() > self.rightRate:
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