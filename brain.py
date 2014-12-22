# -*- coding: utf-8 -*-
from codevs import *
import stage
import random


class Brain():
    def __init__(self):
        self.aStage = stage.Stage()
        self.actions = []

    def startTurn(self):
        self.aStage.startTurn()
        self.actions = []
        self.checkVisitPoint()
        self.ai()

    def ai(self):
        # 順番考える
        self.work()
        self.product()
        self.base()
        self.force()

    def product(self):
        for production in self.aStage.productions:
            if len(self.aStage.workers) < 100:  # 後で定数化
                if self.aStage.resourceNum >= Cost[UnitType.WORKER.value]:
                    self.actions.append((production.cid, UnitType.WORKER.value))
                    self.aStage.resourceNum -= Cost[UnitType.WORKER.value]
                    continue

    def base(self):
        for base in self.aStage.bases:
            if self.aStage.resourceNum >= Cost[UnitType.ASSASSIN.value]:
                if len(self.aStage.knights) < 10:
                    self.actions.append((base.cid, UnitType.KNIGHT.value))
                    self.aStage.resourceNum -= Cost[UnitType.KNIGHT.value]
                else:
                    self.actions.append((base.cid, UnitType.FIGHTER.value))
                    self.aStage.resourceNum -= Cost[UnitType.FIGHTER.value]

    def force(self):
        for force in self.aStage.forces:
            d = None
            if force.cid % 2 == 0:
                self.aStage.castlePoint(force)
                d = force.goToPoint(force.goal[0])
            else:
                d = force.goToPoint(self.aStage.castle.point)
            if d:
                self.actions.append((force.cid, d))


    def work(self):
        for worker in self.aStage.workers:
            d = False
            if worker.point == self.aStage.castle.point and self.aStage.resourceNum > Cost[UnitType.BASE.value] and len(self.aStage.bases) < 2:
                d = UnitType.BASE.value
                self.aStage.resourceNum -= Cost[UnitType.BASE.value]
            else:
                self.checkPoint(worker)
                if not worker.isFix:
                    self.aStage.nearestResouce(worker)
                d = worker.goToPoint(worker.goal[0])

            if d:
                self.actions.append((worker.cid, d))


    def checkVisitPoint(self):
        field = self.aStage.field
        r = [[1, 1], [1, -1], [-1, 1], [-1, -1]]

        GRID = self.aStage.GRID
        for unit in self.aStage.units.values():
            for i in xrange(Range[unit.type.value] + 1):
                for j in xrange(Range[unit.type.value] - i + 1):
                    for x, y in r:
                        xx = unit.point.x + i * x
                        yy = unit.point.y + j * y
                        if 0 <= xx < 100 and xx % GRID == 0 and 0 <= yy < 100 and yy % GRID == 0:
                            field[xx / GRID][yy / GRID] = 2
        # for fi in field:
        #     for f in fi:
        #         print f,
        #     print

    def checkPoint(self, character):
        if not character.isFix and character.goal and character.goal[0] == character.point:
            character.goal.pop(0)