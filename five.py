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
        if self.brain.isAttack:
            pioneerNum = 5
        # elif len(workers) > 30:
        #     pioneerNum = 3

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

class Force(DefaultForce):
    pass

class Base(DefaultBase):
    pass

class Product(DefaultProduct):
    pass