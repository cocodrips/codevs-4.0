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
    pass

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
        if resources and len(forces) > 10: # and force.type == UnitType.ASSASSIN:
            force.forceType = ForceType.HOUSE_SITTING
        elif force.type == UnitType.KNIGHT and len(self.brain.forceUnit(self.brain.unit(UnitType.KNIGHT),
                                                                        ForceType.GATEKEEPER)) < GATEKEEPERS and len(
            forces) > 20:
            force.forceType = ForceType.GATEKEEPER
        else:
            if not self.brain.enemyCastle and not self.brain.defenceMode and len(forces) < FORCE_EXPLORER_NUM:
                force.forceType = ForceType.CASTLE_EXPLORER
            if self.brain.aStage.turnNum % GROUP_INTERVAL == 0:
                if int(self.brain.aStage.turnNum % (
                        GROUP_INTERVAL * 4) < 2) and self.brain.aStage.supporter.aroundStrength(
                    self.brain.castle.point, DEFENCE_RANGE) < self.brain.aStage.enemies.aroundStrength(
                    self.brain.castle.point,
                    DEFENCE_RANGE):
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
        self.brain.aStage.castlePoint(force)
        return force.goToPoint(force.goal[0])


class Base(DefaultBase):
    def noCastle(self, base):
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
        t = self.brain.weakType.value
        self.brain.actions[base.cid] = t
        self.brain.aStage.resourceNum -= Cost[t]


class Product(DefaultProduct):
    pass