class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "({},{})".format(self.x, self.y)

    def __cmp__(self):
        return self.x + self.y

    def __hash__(self):
        return self.x * 1000 + self.y

    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

