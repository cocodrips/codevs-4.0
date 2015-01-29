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
    pass

class Base(DefaultBase):
    pass

class Product(DefaultProduct):
    pass