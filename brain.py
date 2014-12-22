# -*- coding: utf-8 -*-
from codevs import *
import stage


class Brain():
    def __init__(self):
        self.aStage = stage.Stage()
        self.actions = []

    def startTurn(self, time, stageNum, turnNum, units, enemies, resources):
        self.aStage.startTurn(time, stageNum, turnNum, units, enemies, resources)
        self.actions = []
        self.ai()

    def ai(self):
        self.work()
        self.product()

    def product(self):
        for production in self.aStage.productions:
            if self.aStage.resources >= Cost[UnitType.WORKER.value]:
                if len(self.aStage.workers) < 20: # 後で定数化
                    self.actions.append((production.cid, UnitType.WORKER.value))
                    self.aStage.resources -= Cost[UnitType.WORKER.value]

    def work(self):
        for worker in self.aStage.workers:
            d = False
            if self.aStage.resources < Cost[UnitType.BASE.value] or len(self.aStage.bases) > 0:
                d = self.goToNearestResource(worker)
            else:
                d = UnitType.BASE
                self.aStage.resources -= Cost[UnitType.BASE.value]
            if d:
               self.actions.append((worker.cid, d))

    def goToNearestResource(self, character):
        point = self.aStage.nearestResouce(character)
        return character.goToPoint(point)
