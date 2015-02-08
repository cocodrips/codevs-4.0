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
        # if len(workers) > 30:
        # pioneerNum = 3

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

    def canBuild(self):
        if not self.brain.isAttack:
            return False
        if self.brain.aStage.resourceNum < Cost[UnitType.BASE] + 200 * int(self.brain.aStage.five):
            return False
        if len(self.brain.unit(UnitType.BASE)) > 0 and self.brain.aStage.resourceNum < Cost[UnitType.BASE.value] * 2:
            return False
        return True

    def canBuild(self):
        # lila
        if not self.brain.isAttack:
            return False
        if self.brain.aStage.resourceNum < Cost[UnitType.BASE] + 200 * int(self.brain.aStage.five):
            return False
        if len(self.brain.unit(UnitType.BASE)) > 0 and self.brain.aStage.resourceNum < Cost[UnitType.BASE.value] + 100:
            return False
        return True

    def buildBase(self, workers):
        if len(self.brain.unit(UnitType.BASE)) > 0:
            worker = min(workers, key=lambda x: x.point.dist(self.brain.castle.point))
        else:
            zero = Point(60, 60)
            worker = min(workers, key=lambda x: x.point.dist(zero))

        self.brain.actions[worker.cid] = UnitType.BASE.value
        self.brain.aStage.resourceNum -= Cost[UnitType.BASE]
        workers.remove(worker)


class Force(DefaultForce):
    def unsafetyResource(self):
        r = []
        for resource in self.brain.resources:
            resource.mother = [m for m in resource.mother if self.brain.aStage.supporter.units.get(m.cid)]
            if len(resource.mother) > 3:
                continue
            diff = sum([Strength[m.type.value] for m in resource.mother]) < self.brain.aStage.enemies.aroundStrength(
                resource.point, 5)
            if not resource.mother or diff > 400:
                r.append((resource, diff))

        return r

    def houseSitting(self, force, resources):
        self.check(force)
        resources.sort(key=lambda x: x[0].point.dist(force.point))
        if not force.goal and resources:
            for r in resources:
                if len(r[0].mother) < 3:
                    r[0].mother.append(force)
                    force.goal.append(r[0].point)
                    break
                else:
                    resources.remove(r)

        d = ""
        if force.goal:
            d = force.goToPoint(force.goal[0])
        if not d:
            p, strength = self.brain.aStage.enemies.strongest(force.point, Range[force.forceType])
            if strength > GATEKEEP_STRENGTH:
                d = force.goToPoint(p)
        if not d:
            d = force.goToPoint(Point(force.cid % 2 * (MAPSIZE - 1), (1 - force.cid % 2) * (MAPSIZE - 1)))
        return d

    def neet(self, force, forces, resources):
        if resources and len(forces) > 10 and force.type == UnitType.ASSASSIN:
            force.forceType = ForceType.HOUSE_SITTING
        elif force.type == UnitType.KNIGHT and len(self.brain.forceUnit(self.brain.unit(UnitType.KNIGHT),
                                                                        ForceType.GATEKEEPER)) < GATEKEEPERS and len(
            forces) > 20:
            force.forceType = ForceType.GATEKEEPER
        else:
            if not self.brain.enemyCastle and len(forces) < FORCE_EXPLORER_NUM:
                force.forceType = ForceType.CASTLE_EXPLORER
            if self.brain.aStage.turnNum % GROUP_INTERVAL == 0:
                if len(self.brain.forceUnit(self.brain.forces, ForceType.GATEKEEPER)) < 250:
                    force.forceType = ForceType.GATEKEEPER
                elif force.point.dist(self.brain.castle.point) < 10:
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

    def attack(self, force):
        if len(self.brain.forceUnit(self.brain.forces, ForceType.GATEKEEPER)) < 100:
            # if self.brain.castle.point:
            force.forceType = ForceType.HOUSE_SITTING
                # force.goal = []
            return
        self.brain.aStage.castlePoint(force)
        return force.goToPoint(force.goal[0])


class Base(DefaultBase):
    def noCastle(self, base):
        # 城みつからなくてもデフォルトに移行
        if self.brain.aStage.turnNum > 200:
            return False
        if self.brain.aStage.resourceNum < Cost[UnitType.KNIGHT.value]:
            return False
        if self.brain.aStage.resourceNum >= Cost[UnitType.ASSASSIN.value] and self.brain.aStage.five and self.brain.aStage.enemies.forces():
            t = UnitType.FIGHTER.value
        else:
            if self.brain.aStage.resourceNum >= Cost[UnitType.ASSASSIN.value]:
                t = UnitType.ASSASSIN.value
            else:
                t = UnitType.KNIGHT.value  # + random.randint(0, 1)
        self.brain.actions[base.cid] = t
        self.brain.aStage.resourceNum -= Cost[t]
        return True

    def default(self, base):
        if self.brain.aStage.resourceNum < Cost[self.brain.weakType.value]:
            return False
        if len(self.brain.unit(UnitType.BASE)) < 2:
            return False
        t = self.brain.weakType.value
        self.brain.actions[base.cid] = t
        self.brain.aStage.resourceNum -= Cost[t]


class Product(DefaultProduct):
    pass