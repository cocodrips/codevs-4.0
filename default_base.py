# -*- coding: utf-8 -*-
from codevs import *
from model import Point
import sys

class DefaultBase(object):
    def __init__(self, brain):
        """
        :type brain: brain.Brain
        """
        self.brain = brain

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

    def housesit(self, base):
        resources = self.unsafetyResource()
        forces = self.brain.forces
        if len(forces) < 20:
            return False
        if not resources:
            return False
        if self.brain.aStage.resourceNum > Cost[UnitType.ASSASSIN.value]:
            t = UnitType.ASSASSIN.value
            self.brain.actions[base.cid] = t
            self.brain.aStage.resourceNum -= Cost[t]
        return True

    def default(self, base):
        if self.brain.aStage.resourceNum < Cost[self.brain.weakType.value]:
            return False

        t = self.brain.weakType.value
        self.brain.actions[base.cid] = t
        self.brain.aStage.resourceNum -= Cost[t]

    def unsafetyResource(self):
        r = []
        for resource in self.brain.resources:
            resource.mother = [m for m in resource.mother if self.brain.aStage.supporter.units.get(m.cid)]
            if len(resource.mother) > 3:
                continue
            diff = sum([Strength[m.type.value] for m in resource.mother]) < self.brain.aStage.enemies.aroundStrength(
                resource.point, 5)
            if not resource.mother:
                r.append((resource, diff))

        return r