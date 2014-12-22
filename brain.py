# -*- coding: utf-8 -*-
from codevs import *
import stage


class Brain():
    def __init__(self):
        self.aStage = stage.Stage()
        self.actions = []

    def startTurn(self, time, stageNum, turnNum, resourceNum, units, enemies, resources):
        self.aStage.startTurn(time, stageNum, turnNum, resourceNum, units, enemies, resources)
        self.actions = []
        self.ai()

    def ai(self):
        #順番考える
        self.work()
        self.product()
        self.base()
        self.force()

    def product(self):
        for production in self.aStage.productions:
            if len(self.aStage.workers) < 40: # 後で定数化
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
            point = self.aStage.castlePoint(force)
            d = force.goToPoint(point)
            if d:
                self.actions.append((force.cid, d))


    def work(self):
        for worker in self.aStage.workers:
            d = False
            if self.aStage.resourceNum < Cost[UnitType.BASE.value] or len(self.aStage.bases) > 0:
                d = self.goToNearestResource(worker)
            else:
                d = UnitType.BASE.value
                self.aStage.resourceNum -= Cost[UnitType.BASE.value]
            if d:
               self.actions.append((worker.cid, d))

    def goToNearestResource(self, character):
        point = self.aStage.nearestResouce(character)
        return character.goToPoint(point)
