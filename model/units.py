from codevs import *
from model import Point


class Units:
    def __init__(self):
        self.map = None
        self.strengthMap = {}
        self.units = {}
        self.castle = None
        self.unit = [[] for unitType in UnitType]

    def turnInitialize(self, turnNum=10):
        self.unit = [[] for unitType in UnitType]
        self.update()
        self._aroundStrength = {}
        self._strongest = None
        if turnNum == 0:
            i = 0
            zero = self.unit[UnitType.CASTLE][0].point
            for worker in self.unit[UnitType.WORKER]:
                width = i * 18
                worker.goal = [Point(width + 2, zero.y),
                               Point(width + 2, 99 - 11 * i),
                               Point(width + 11, 99 - 11 * i),
                               Point(width + 11, 0)]
                i += 1


    def update(self):
        map = [[0 for _ in xrange(100)] for _ in xrange(100)]
        for unit in self.units.values():
            v = unit.type.value
            self.unit[v].append(unit)
            r = AttackRange[v]

            for i in xrange(-r, r + 1):
                rr = r - abs(i)
                for j in xrange(-rr, rr + 1):
                    x = unit.point.x + i
                    y = unit.point.y + j

                    if 0 <= x < 100 and 0 <= y < 100:
                        map[x][y] += Strength[v] / (abs(i) + abs(j) + 1)
        self.map = map
        self.strengthMap = self.cumulativeSumTable(map)

    def aroundStrength(self, point, size):
        if self._aroundStrength.get((point, size)):
            return self._aroundStrength[(point, size)]
        p1 = Point(point.x - size, point.y - size)
        p2 = Point(point.x + size, point.y + size)

        self._aroundStrength[(point, size)] = self.rangeStrength(p1, p2)
        return self._aroundStrength[(point, size)]

    def strongest(self):
        if not self._strongest:
            maxi = -1
            point = None
            for i in xrange(MAPSIZE):
                for j in xrange(MAPSIZE):
                    if maxi < self.map[i][j]:
                        maxi = self.map[i][j]
                        point = Point(i, j)
            self._strongest = point
        return self._strongest


    def rangeStrength(self, p1, p2):
        p2.x = min(MAPSIZE - 1, p2.x)
        p2.y = min(MAPSIZE - 1, p2.y)
        s = self.strengthMap[p2.x][p2.y]
        if p1.x > 0:
            s -= self.strengthMap[p1.x - 1][p2.y]
        if p1.y > 0:
            s -= self.strengthMap[p2.x][p1.y - 1]
        if p1.x > 0 and p1.y > 0:
            s += self.strengthMap[p1.x - 1][p1.y - 1]
        return s

    def cumulativeSumTable(self, map):
        strengthMap = [[0 for _ in xrange(MAPSIZE)] for _ in xrange(MAPSIZE)]
        for r in xrange(MAPSIZE):
            for c in xrange(MAPSIZE):
                total = 0
                if c != 0:
                    total += strengthMap[r][c - 1]
                if r != 0:
                    total += strengthMap[r - 1][c]
                if c != 0 and r != 0:
                    total -= strengthMap[r - 1][c - 1]
                strengthMap[r][c] = total + map[r][c]
        return strengthMap


