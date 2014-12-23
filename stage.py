# -*- coding: utf-8 -*-

from codevs import *
from model import Point, Units
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

        self.GRID = 4
        self.field = [[0 for _ in xrange(100 / self.GRID)] for _ in xrange(100 / self.GRID)]

    def startTurn(self):
        if self.turnNum > 200:
            self.workerThrehold = 7

        # Initialize units.
        self.supporter.turnInitialize(self.turnNum)
        self.enemies.turnInitialize()
        self.updateVisitPoint()

        self._searchPoints = []

    def nearestResouce(self, character):
        closest = None
        minD = INF

        for resource, charas in self.resources.items():
            d = resource.dist(character.point)
            if d < minD and len(charas) < self.workerThrehold:
                closest = resource
                minD = d

        if closest and character.goal:
            if character.point.dist(character.goal[0]) < closest.dist(character.point):
                closest = None

        if not closest:
            if not character.goal:
                point = self.randomAction(character)
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

        if not character.goal:
            character.goal.append(Point(99 - character.cid % 40, 99 - random.randint(0, 10)))

    def updateUnits(self):
        for k, v in self.resources.items():
            self.resources[k] = [chara for chara in v if chara.turn == self.turnNum]

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

