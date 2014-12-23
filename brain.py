# -*- coding: utf-8 -*-
from codevs import *
from model import Point
import stage
import random


class Brain():
    def __init__(self):
        self.aStage = stage.Stage()
        self.actions = []

    def startTurn(self):
        self.aStage.startTurn()
        self.actions = {}
        self.ai()

    def ai(self):
        # 順番考える
        self.work()
        self.product()
        self.base()
        self.force()

    def product(self):
        for production in self.aStage.supporter.unit[UnitType.CASTLE]:
            if self.aStage.turnNum % 3 == 0:
                return

            if self.aStage.resourceNum < Cost[UnitType.WORKER.value]:
                return

            if len(self.aStage.supporter.unit[UnitType.WORKER]) > 50:
                continue

            p1 = production.point.plus(Point(-20, -20))
            p2 = production.point.plus(Point(20, 20))
            if self.aStage.enemies.rangeStrength(p1, p2) < 300:  # 後で定数化
                self.actions[production.cid] = UnitType.WORKER.value
                self.aStage.resourceNum -= Cost[UnitType.WORKER.value]

    def base(self):
        for base in self.aStage.supporter.unit[UnitType.BASE]:
            if self.aStage.resourceNum < Cost[UnitType.ASSASSIN.value]:
                return
            if len(self.aStage.supporter.unit[UnitType.KNIGHT]) < 20:
                self.actions[base.cid] = UnitType.KNIGHT.value
                self.aStage.resourceNum -= Cost[UnitType.KNIGHT.value]
            else:
                t = UnitType.FIGHTER.value + random.randint(0, 1)
                self.actions[base.cid] = t
                self.aStage.resourceNum -= Cost[t]

    def knight(self):
        for knight in self.aStage.supporter.unit[UnitType.KNIGHT]:
            pass

    def force(self):
        units = self.aStage.supporter.unit
        forces = units[UnitType.ASSASSIN] + units[UnitType.FIGHTER]
        castlePoint = self.aStage.supporter.unit[UnitType.CASTLE][0].point

        searchPoints = [self.aStage.field]
        for force in forces:
            d = None
            if force.cid % 5 < 3:
                self.aStage.castlePoint(force)
                d = force.goToPoint(force.goal[0])
            else:  # 防衛班
                point = castlePoint.plus(Point(2 * force.cid % 5, 2 * force.cid / 5 % 5))
                d = force.goToPoint(point)
            if d:
                self.actions[force.cid] = d

    def work(self):
        # workers = [i for i in self.aStage.supporter.unit[UnitType.WORKER] if not i.isFix]
        bases = self.aStage.supporter.unit[UnitType.BASE]
        workers = self.aStage.supporter.unit[UnitType.WORKER]
        castlePoint = self.aStage.supporter.unit[UnitType.CASTLE][0].point
        for worker in workers:
            d = False
            if worker.point == castlePoint and self.aStage.resourceNum > Cost[UnitType.BASE.value] and len(bases) < 2:
                d = UnitType.BASE.value
                self.aStage.resourceNum -= Cost[UnitType.BASE.value]

            else:
                self.checkPoint(worker)
                if not worker.goal:
                    self.aStage.nearestResouce(worker)
                d = worker.goToPoint(worker.goal[0])

            if d:
                self.actions[worker.cid] = d

    def checkPoint(self, character):
        if not character.isFix and character.goal and character.goal[0] == character.point:
            character.goal.pop(0)