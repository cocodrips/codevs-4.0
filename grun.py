# -*- coding: utf-8 -*-
from codevs import *
from model import Point
import sys


def order(self):
    """
    :type self:brain.Brain
    """

    self.isAttack = len(self.unit(UnitType.WORKER)) > INCOME
    self.defenceMode = self.aStage.enemies.aroundStrength(self.castle.point,
                                                          Range[UnitType.CASTLE]) > DEFENCE_THRESHOLD

    self.work()
    self.product()
    self.base()
    self.force()