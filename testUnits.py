from codevs import *
from model import Point, Character
import unittest
import units


class UnitsTestCase(unittest.TestCase):
    def setUp(self):
        self.units = units.Units()

    def testUpdate(self):
        self.units.units = {1: Character(1, 10, 10, 2000, UnitType.WORKER),
                            2: Character(1, 10, 10, 2000, UnitType.CASTLE)}
        self.units.update()
        # for i in self.units.strengthMap:
        #     for j in i:
        #         print j,
        #     print i
        # print self.units.unit
        self.assertEqual(len(self.units.unit[UnitType.CASTLE.value]), 1)

    def testRangeStrength(self):
        table = [[1 for j in xrange(100)] for i in xrange(100)]
        self.units.strengthMap = self.units.cumulativeSumTable(table)
        target = self.units.rangeStrength(Point(50, 50), Point(99, 99))
        self.assertEqual(target, 2500)

    def testCumulativeSum(self):
        table = [[1 for j in xrange(100)] for i in xrange(100)]
        target = self.units.cumulativeSumTable(table)
        self.assertEqual(target[99][99], 10000)


if __name__ == '__main__':
    unittest.main()
