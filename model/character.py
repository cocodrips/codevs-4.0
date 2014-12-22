from point import Point
import random

class Character(object):
    def __init__(self, cid, y, x, hp, type):
        self.cid = cid
        self.point = Point(x, y)
        self.hp = hp
        self.type = type
        self.goal = None

    def goToPoint(self, point):
        if random.random() < 0.5:
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
        self.goal = None
        return False

    def distanceToCharacter(self, character):
        pass

    def closest(self, field):
        pass