# -*- coding: utf-8 -*-

from codevs import *
from model import Point, Units, Resource
import random


class Stage(object):
    def __init__(self):
        self.time = 0
        self.stageNum = 0
        self.turnNum = 0
        self.workerThrehold = 5
        self.resourceNum = 0

        self.supporter = Units()
        self.enemies = Units()

        self.resources = {}
        self.nearestResouces = {}

        self.GRID = 10
        self.field = [[0 for _ in xrange(100 / self.GRID)] for _ in xrange(100 / self.GRID)]


    def startTurn(self):
        # Initialize units.
        self.supporter.turnInitialize(self.turnNum)
        self.enemies.turnInitialize()
        self.updateVisitPoint()
        self.updateUnits()

        self._searchPoints = []

    def nearestResouce(self, character):
        closest = None
        minD = INF

        for resource, charas in self.resources.items():
            d = resource.dist(character.point)
            if d < minD and len(charas) < self.workerThrehold and self.enemies.aroundStrength(resource, 5) < 5000:
                closest = resource
                minD = d

        if closest and character.goal:
            if character.point.dist(character.goal[0]) < self.supporter.unit[UnitType.CASTLE][0].point.dist(closest):
                closest = None

        if not closest:
            if not character.goal:
                point = self.randomAction(character)
                if not point:  # 全部回ってると起動するか考える
                    return character.goal.append(character.point)

                character.goal.append(Point(point.x, character.point.y))
                character.goal.append(point)
            return

        self.resources[closest].append(character)
        if character.goal:
            # 行く場所をすでに仮ぎめしてたらキャンセル
            if self.field[character.goal[-1].x / self.GRID][character.goal[-1].y / self.GRID] == 1:
                self.field[character.goal[-1].x / self.GRID][character.goal[-1].y / self.GRID] = 0
        character.goal = [closest]
        character.isFix = True

    def randomAction(self, character):
        closest = None
        d = INF
        for i in xrange(100 / self.GRID):
            for j in xrange(100 / self.GRID):
                if self.field[i][j] == 0:
                    point = Point(i * self.GRID, j * self.GRID)
                    dist = character.point.dist(point)
                    if dist < d:
                        d = dist
                        closest = point

        if closest and d < 70:
            self.field[closest.x / self.GRID][closest.y / self.GRID] = 1
        return closest


    def castlePoint(self, character):
        castle = self.enemies.unit[UnitType.CASTLE.value]
        if castle:
            character.goal = [castle[0].point]
            character.isFix = True
            return

        if character.goal and character.goal[0] == character.point:
            strongestPoint, strength = self.enemies.strongest(character.point, 5)
            character.goal.append(strongestPoint)
            character.goal.pop(0)

        if not character.goal:
            character.goal.append(Point(MAPSIZE - 5 - self.turnNum % 20, MAPSIZE - 5 - self.turnNum % 20))


    def updateVisitPoint(self):
        for i in xrange(MAPSIZE / self.GRID):
            for j in xrange(MAPSIZE / self.GRID):
                if self.supporter.map[i * self.GRID][j * self.GRID] > 0:
                    self.field[i][j] = True

    def searchPoints(self):
        if self.searchPoints:
            return self.searchPoints()
        searchPoints = []
        for i in xrange(MAPSIZE / self.GRID):
            for j in xrange(MAPSIZE / self.GRID):
                if self.field[i][j] == 0:
                    searchPoints.append(Point(i * MAPSIZE, j * MAPSIZE))
        self._searchPoints = searchPoints
        return searchPoints

    def emptyResources(self):
        return [r for r in self.resources.values() if len(r.volunteer) < self.workerThrehold]

    # Update & Reset
    def updateUnits(self):
        for v in self.resources.values():
            v.reset()

    # controller.py
    def updateResource(self, point):
        """
        Call from controller.py.
        """
        if point not in self.resources:
            self.resources[point] = Resource(point)