from codevs import *
from model import Point


class Stage(object):
    def __init__(self):
        self.time = 0
        self.stageNum = 0
        self.turnNum = 0
        self.enemyCastle = None

        self.units = []
        self.enemies = []
        self.workers = []
        self.resources = {}
        self.nearestResouces = {}

    def startTurn(self, time, stageNum, turnNum, resourceNum, units, enemies, resources):
        self.time = time
        self.stageNum = stageNum
        self.turnNum = turnNum
        self.resourceNum = resourceNum
        self.units = units
        self.enemies = enemies

        # Initialize units.
        self.workers = []
        self.productions = []
        self.forces = []
        self.bases = []
        self.knights = []
        self.castle = None
        self.updateUnits()


        for resource in resources:
            if resource not in self.resources:
                self.resources[resource] = 0

    def nearestResouce(self, character):
        if self.nearestResouces.get(character.point):
            return self.nearestResouces.get(character.point)

        closest = None
        minD = INF
        for resource, count in self.resources.items():
            d = resource.dist(character.point)
            if d < minD:
                closest = resource
                minD = d

        if not closest:
            return Point(character.point.x - 10, character.point.y - character.cid % 10)

        self.nearestResouces[character.point] = closest
        return closest

    def castlePoint(self, character):
        if not self.enemyCastle:
            for enemy in self.enemies:
                if enemy.type == UnitType.CASTLE:
                    self.enemyCastle = enemy.point
                    break

        if self.enemyCastle:
            return self.enemyCastle

        return Point(character.cid % 40, character.cid % 20)

    def updateUnits(self):
        for unit in self.units:
            if unit.type == UnitType.WORKER:
                self.workers.append(unit)
            if unit.type == UnitType.ASSASSIN:
                self.forces.append(unit)
            if unit.type == UnitType.FIGHTER:
                self.forces.append(unit)
            if unit.type == UnitType.KNIGHT:
                self.knights.append(unit)
                self.forces.append(unit)
            if unit.type == UnitType.CASTLE:
                self.castle = unit
                self.productions.append(unit)
            if unit.type == UnitType.VILLAGE:
                self.productions.append(unit)
            if unit.type == UnitType.BASE:
                self.bases.append(unit)









