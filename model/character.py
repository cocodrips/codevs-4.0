from point import Point

class Character(object):
    def ___init__(self, cid, y, x, hp, type):
        self.cid = cid
        self.point = Point(x, y)
        self.hp = hp
        self.type = type

    def goToPoint(self, point):
        if point.x - self.point.x > 0:
            return 'R'
        if point.x - self.point.x < 0:
            return 'L'
        if point.y - self.point.y > 0:
            return 'D'
        if point.y - self.point.t < 0:
            return 'U'
        return False

    def distanceToCharacter(self, character):
        pass

    def closest(self, field):
        pass