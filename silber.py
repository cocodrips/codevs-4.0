# -*- coding: utf-8 -*-
from codevs import *
from model import Point
import sys

from default_worker import DefaultWorker
from default_force import DefaultForce
from default_product import DefaultProduct
from default_base import DefaultBase


def order(self):
    """
    :type self:brain.Brain
    """

    self.isAttack = len(self.unit(UnitType.WORKER)) > INCOME
    self.work(Worker(self))
    self.product(Product(self))
    self.base(Base(self))
    self.force(Force(self))

class Worker(DefaultWorker):
    def selectPioneer(self, workers):
        pioneers = self.brain.forceUnit(workers, ForceType.PIONEER)
        i = len(pioneers)
        table = self.pTable(workers)
        usedWorker, usedPoint = [], []
        pioneerNum = PIONEER_NUM

        for dist, point, worker in table:
            if worker in usedWorker or point in usedPoint:
                continue
            if i > pioneerNum:
                break
            usedWorker.append(worker)
            usedPoint.append(point)
            self.brain.pioneerMap.remove(point)
            worker.forceType = ForceType.PIONEER
            worker.goal.append(point)
            i += 1

    def buildBase(self, workers):
        worker = min(workers, key=lambda x: x.point.dist(self.brain.castle.point))
        self.brain.actions[worker.cid] = UnitType.BASE.value
        self.brain.aStage.resourceNum -= Cost[UnitType.BASE]
        workers.remove(worker)


class Force(DefaultForce):
    def neet(self, force, forces, resources):
        if resources and len(forces) > 20 and force.type == UnitType.ASSASSIN:
            force.forceType = ForceType.HOUSE_SITTING
        elif self.brain.aStage.turnNum % GROUP_INTERVAL == 0: # 資源で数かえる
            if len(self.brain.forceUnit(self.brain.forces, ForceType.GATEKEEPER)) < 200:
                force.forceType = ForceType.GATEKEEPER
            else:
                force.forceType = ForceType.ATTACKER

            force.rightRate = int(self.brain.aStage.turnNum % (GROUP_INTERVAL * 2) == 0)

    def gatekeeper(self, force):
        point = self.brain.castle.point
        p, strength = self.brain.aStage.enemies.strongest(point, Range[UnitType.CASTLE])
        if force.point.dist(self.brain.castle.point) <  Range[UnitType.CASTLE] and strength > GATEKEEP_STRENGTH:
            point = p
        p, strength = self.brain.aStage.enemies.strongest(force.point, Range[force.type])
        if strength > 500:
            point = p
        return force.goToPoint(point)


class Base(DefaultBase):
    def noCastle(self, base):
        return False

    def default(self, base):
        if self.brain.aStage.resourceNum < Cost[self.brain.weakType.value] + Cost[UnitType.WORKER]:
            return False
        t = self.brain.weakType.value
        self.brain.actions[base.cid] = t
        self.brain.aStage.resourceNum -= Cost[t]

class Product(DefaultProduct):
    pass