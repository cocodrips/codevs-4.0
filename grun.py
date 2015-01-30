# -*- coding: utf-8 -*-
from codevs import *
from model import Point
import sys
import random

from default_worker import DefaultWorker
from default_force import DefaultForce
from default_product import DefaultProduct
from default_base import DefaultBase

GG = 5

def order(self):
    """
    :type self:brain.Brain
    """
    v = self.aStage.enemies.unit[UnitType.VILLAGE][0]
    b = self.unit(UnitType.BASE)
    self.v= v.point.plus(Point(GG, 0))
    # if b:
    #     self.v = v.point.plus(min([p for p in [Point(GG, 0), Point(0, GG)]], key=lambda x:b[0].point.dist(v.point.plus(x))))
    self.nNum = len(self.forceUnit(self.forces, ForceType.GRUNRUN))
    # print >> sys.stderr, self.aStage.turnNum, self.nNum

    self.isAttack = len(self.unit(UnitType.WORKER)) > INCOME
    self.work(Worker(self))
    self.product(Product(self))
    self.base(Base(self))
    self.force(Force(self))


class Worker(DefaultWorker):

    def buildBase(self, workers):
        zero = self.brain.v
        worker = min(workers, key=lambda x: x.point.dist(zero))

        self.brain.actions[worker.cid] = UnitType.BASE.value
        self.brain.aStage.resourceNum -= Cost[UnitType.BASE]
        workers.remove(worker)
    def actWorker(self, fWorkers):
        """
        Workerの動きを決定する
        """
        table = self.rtTable(fWorkers)
        used = set()
        for dist, resource, worker in table:
            # 0: distance, 1:resource, 2:worker
            if worker not in used and len(resource.volunteer) < self.brain.aStage.workerThrehold:
                d = worker.goToPoint(resource.point)
                used.add(worker)
                if d:
                    self.brain.actions[worker.cid] = d
                    resource.planners.append(worker)
                else:
                    # on resource
                    # 逃げる
                    if self.brain.aStage.enemies.aroundStrength(resource.point,Range[UnitType.WORKER]) > 500:

                        p = self.brain.aStage.enemies.weakestDirection(resource.point)
                        d = worker.goToPoint(p)
                        resource.planners.append(worker)
                    # 逃げない
                    else:
                        if len(self.brain.unit(ForceType.WORKER)) < INCOME and distToUnits(worker.point,
                                                                                           self.brain.productions) >= PRODUCTION_INTERVAL and self.brain.aStage.enemies.aroundStrength(worker.point, 6) < 1000 and self.brain.aStage.resourceNum >= Range[UnitType.VILLAGE.value]:
                            self.brain.actions[worker.cid] = UnitType.VILLAGE.value
                            self.brain.aStage.resourceNum -= Cost[UnitType.VILLAGE.value]
                        # elif worker.point.x +  worker.point.y > 160 and self.brain.aStage.resourceNum >= Range[UnitType.VILLAGE.value]:
                        #     self.brain.actions[worker.cid] = UnitType.VILLAGE.value
                        #     self.brain.aStage.resourceNum -= Cost[UnitType.VILLAGE.value]
                        resource.workers.append(worker)

        for worker in fWorkers:
            if worker not in used and distToUnits(worker.point, self.brain.resources) != 0:
                d = worker.goToPoint(self.brain.aStage.enemies.strongest(worker.point, 5)[0])
                if d:
                    self.brain.actions[worker.cid] = d

class Force(DefaultForce):
    def neet(self, force, forces, resources):
        # p = min([Point(8, 0), Point(0, 8), Point(0, -8), Point(-8, 0)], key=lambda x: force.point.dist(v.point.plus(x)))
        # p = v.point.plus(p)
        if resources and len(forces) > 10 and force.type == UnitType.ASSASSIN:
            force.forceType = ForceType.HOUSE_SITTING
        if self.brain.nNum < 10:
            force.forceType = ForceType.GRUNRUN
            return
        elif force.type == UnitType.KNIGHT and len(self.brain.forceUnit(self.brain.unit(UnitType.KNIGHT),
                                                                        ForceType.GATEKEEPER)) < GATEKEEPERS and len(
            forces) > 20:
            force.forceType = ForceType.GATEKEEPER
        else:
            if not self.brain.enemyCastle and not self.brain.defenceMode and len(forces) < FORCE_EXPLORER_NUM:
                force.forceType = ForceType.CASTLE_EXPLORER
            if self.brain.aStage.turnNum % GROUP_INTERVAL == 0: #and force.point == p:
                if int(self.brain.aStage.turnNum % (
                        GROUP_INTERVAL * 4) < 2) and self.brain.aStage.supporter.aroundStrength(
                    self.brain.castle.point, DEFENCE_RANGE) < self.brain.aStage.enemies.aroundStrength(
                    self.brain.castle.point,
                    DEFENCE_RANGE):
                    force.forceType = ForceType.GATEKEEPER
                else:
                    force.forceType = ForceType.ATTACKER
                force.rightRate = int(self.brain.aStage.turnNum % (GROUP_INTERVAL * 2) == 0)
            # else:
            #     return force.goToPoint(p)

    def grunrun(self, force):
        return force.goToPoint(self.brain.v)



class Base(DefaultBase):
    pass

class Product(DefaultProduct):
    pass


