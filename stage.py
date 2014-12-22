# -*- coding: utf-8 -*-

from codevs import *
from model import Point
import random


class Stage(object):
    def __init__(self):
        self.time = 0
        self.stageNum = 0
        self.turnNum = 0
        self.workerThrehold = 5
        self.enemyCastle = None

        self.units = {}
        self.enemies = {}
        self.workers = []
        self.resources = {}
        self.nearestResouces = {}

        self.GRID = 4
        self.field = [[0 for _ in xrange(100/self.GRID)] for _ in xrange(100/self.GRID)]

    def startTurn(self):
        if self.turnNum > 200:
            self.workerThrehold = 7

        # Initialize units.
        self.workers = []
        self.productions = []
        self.forces = []
        self.bases = []
        self.knights = []
        self.castle = None
        self.updateUnits()

    def nearestResouce(self, character):
        closest = None
        minD = INF

        for resource, charas in self.resources.items():
            d = resource.dist(character.point)
            if d < minD and len(charas) < self.workerThrehold:
                closest = resource
                minD = d

        if closest and closest.dist(character.point) < closest.dist(character.point):
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
        for i in xrange(1, 100/self.GRID, 2):
            for j in xrange(100/self.GRID):
                if self.field[i][j] == 0:
                    point = Point(i * self.GRID, j * self.GRID)
                    dist = character.point.dist(point)
                    if dist < d:
                        d = dist
                        closest = point

        if closest and d < 70:
            self.field[closest.x / self.GRID][closest.y / self.GRID] = 1
            self.field[closest.x / self.GRID - 1][closest.y / self.GRID] = 1

        return closest
        return self.castle.point


    def castlePoint(self, character):
        if not self.enemyCastle:
            for enemy in self.enemies.values():
                if enemy.type == UnitType.CASTLE:
                    self.enemyCastle = enemy.point
                    break

        if self.enemyCastle:
            character.goal = [self.enemyCastle]
            character.isFix = True
            return

        if not character.goal:
            character.goal.append(Point(character.cid % 40, random.randint(0, 39)))


    def updateUnits(self):
        for unit in self.units.values():
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

        for k, v in self.resources.items():
            self.resources[k] = [chara for chara in v if chara.turn == self.turnNum]









