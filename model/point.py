class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "({},{})".format(self.x, self.y)

    def __cmp__(self, other):
        return (self.x + self.y) - (other.x + other.y)

    def __hash__(self):
        return self.x * 1000 + self.y

    def plus(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def isRange(self, other, size):
        return self.x - size < other.x < self.x + size and self.y - size < other.y < self.y + size


