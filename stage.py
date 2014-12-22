from codevs import *
from model import Point


class Stage(object):
    def __init__(self):
        self.time = 0
        self.stageNum = 0
        self.turnNum = 0
        self.units = []
        self.enemies = []
        self.workers = []
        self.resources = {}
        self.nearestResouces = {}

    def startTurn(self, time, stageNum, turnNum, units, enemies, resources):
        self.time = time
        self.stageNum = stageNum
        self.turnNum = turnNum
        self.units = units
        self.enemies = enemies

        # Initialize units.
        self.workers = []
        self.productions = []
        self.forces = []
        self.bases = []
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

    def updateUnits(self):
        for unit in self.units:
            if unit.type == UnitType.WORKER:
                self.workers.append(unit)
            if unit.type == UnitType.ASSASSIN:
                self.forces.append(unit)
            if unit.type == UnitType.FIGHTER:
                self.forces.append(unit)
            if unit.type == UnitType.KNIGHT:
                self.forces.append(unit)
            if unit.type == UnitType.CASTLE:
                self.castle = unit
                self.productions.append(unit)
            if unit.type == UnitType.VILLAGE:
                self.productions.append(unit)
            if unit.type == UnitType.BASE:
                self.bases.append(unit)









