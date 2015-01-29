# -*- coding: utf-8 -*-
from codevs import *
from model import Point
import sys

class DefaultProduct(object):
    def __init__(self, brain):
        """
        :type brain: brain.Brain
        """
        self.brain = brain
    
    def generate(self, production):
        margin = len(self.brain.unit(UnitType.BASE)) * Cost[self.brain.weakType.value] + Cost[UnitType.WORKER.value] # len(self.unit(UnitType.BASE)) *

        # 何度も呼ぶので無駄
        if self.brain.aStage.resourceNum >= margin:
            self.brain.aStage.resourceNum -= Cost[UnitType.WORKER.value]
            self.brain.actions[production.cid] = UnitType.WORKER.value
            return True
        return False
    
    def canWait(self):
        if (self.brain.aStage.enemies.aroundStrength(self.brain.castle.point,
                                               5) > 50000 and distToUnits(self.brain.castle.point,
                                                                          self.brain.unit(
                                                                              UnitType.BASE)) != 0):
            return True
        if self.brain.aStage.turnNum == 5:
            return True
        if self.brain.aStage.turnNum < KEEP_WORKER:
            return False
        if len(self.brain.forceUnit(self.brain.unit(UnitType.WORKER), ForceType.GATEKEEPER)) > 0:
            return False
        if len(self.brain.unit(UnitType.BASE)) > 1:
            return False
        return True
