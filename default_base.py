# -*- coding: utf-8 -*-
from codevs import *
from model import Point
import sys

class CommandBase(object):
    def __init__(self, brain):
        """
        :type brain: brain.Brain
        """
        self.brain = brain

    def noCastle(self, base):
        if self.brain.aStage.resourceNum < Cost[UnitType.KNIGHT.value]:
            return
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
        forces = self.brain.forces
        if len(forces) < 20:
            return False
        if self.brain.aStage.resourceNum > Cost[UnitType.ASSASSIN.value]:
            t = UnitType.ASSASSIN.value
            self.brain.actions[base.cid] = t
            self.brain.aStage.resourceNum -= Cost[t]
        return True