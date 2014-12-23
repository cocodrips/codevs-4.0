# -*- coding: utf-8 -*-
from codevs import *
from model import Point
import stage
import random
import sys


class Brain():
    def __init__(self):
        self.aStage = stage.Stage()
        self.actions = []

    def startTurn(self):
        self.aStage.startTurn()
        self.actions = {}
        self.ai()

    def ai(self):
        # 順番考える
        self.work()
        self.product()
        self.base()
        self.force()

    def product(self):
        productions = self.aStage.supporter.unit[UnitType.VILLAGE]
        productions.sort(key=lambda x: (len(self.aStage.resources.get(x.point)),
                                        self.aStage.enemies.aroundStrength(x.point, 5)))  # ワーカーが少ない村に優先的に
        productions += self.aStage.supporter.unit[UnitType.CASTLE]
        for production in productions:
            if self.aStage.turnNum % 3 == 0:
                return

            if self.aStage.resourceNum < Cost[UnitType.WORKER.value]:
                return

            if len(self.aStage.supporter.unit[UnitType.WORKER]) > 100:
                continue

            if self.aStage.enemies.aroundStrength(production.point, 10) < 2000:  # 後で定数化
                self.actions[production.cid] = UnitType.WORKER.value
                self.aStage.resourceNum -= Cost[UnitType.WORKER.value]

    def base(self):
        for base in self.aStage.supporter.unit[UnitType.BASE]:
            if self.aStage.resourceNum < Cost[UnitType.ASSASSIN.value]:
                return
            else:
                t = UnitType.KNIGHT.value + random.randint(0, 2)
                self.actions[base.cid] = t
                self.aStage.resourceNum -= Cost[t]


    def force(self):
        def check(self, character):
            if not character.isFix and character.goal and character.goal[0] == character.point:
                if self.aStage.enemies.aroundStrength(character.point, 2) < 500:
                    character.goal.pop(0)

        def unsafetyResource(self):
            r = []
            for resource in self.aStage.resources:
                s = self.aStage.enemies.aroundStrength(resource, 10)
                if 100 < s:
                    r.append(resource)
            return r

        resources = unsafetyResource(self)
        units = self.aStage.supporter.unit
        forces = units[UnitType.ASSASSIN] + units[UnitType.FIGHTER] + units[UnitType.KNIGHT]
        castlePoint = self.aStage.supporter.unit[UnitType.CASTLE][0].point

        for force in forces:
            d = None
            check(self, force)
            if force.cid % 10 < 7:
                if resources and force.goal:
                    for resource in resources:
                        if force.point.dist(resource) < 15:
                            force.goal = [resource]
                            d = force.goToPoint(force.goal[0])
                            resources.remove(resource)
                            break

                if not d:
                    self.aStage.castlePoint(force)
                    d = force.goToPoint(force.goal[0])
            else:  # 防衛班
                point = castlePoint.plus(Point(2 * force.cid % 5, 2 * force.cid / 5 % 5))
                d = force.goToPoint(point)
            if d:
                self.actions[force.cid] = d

    def work(self):
        # workers = [i for i in self.aStage.supporter.unit[UnitType.WORKER] if not i.isFix]
        bases = self.aStage.supporter.unit[UnitType.BASE]
        workers = self.aStage.supporter.unit[UnitType.WORKER]
        castlePoint = self.aStage.supporter.unit[UnitType.CASTLE][0].point

        buildBase = None
        if Cost[UnitType.BASE.value] < self.aStage.resourceNum:
            buildBase = self.safetyVillage()
            if buildBase:
                sys.stderr.write("plan {},{}\n".format(buildBase.x, buildBase.y))

        for worker in workers:
            d = False
            if worker.point in self.aStage.resources and self.aStage.resourceNum > Cost[
                UnitType.VILLAGE.value] and self.distToVillage(worker) > 70:
                d = UnitType.VILLAGE.value
                self.aStage.resourceNum -= Cost[UnitType.VILLAGE.value]

            elif worker.point == castlePoint and self.aStage.resourceNum > Cost[UnitType.BASE.value] and len(bases) < 1:
                d = UnitType.BASE.value
                self.aStage.resourceNum -= Cost[UnitType.BASE.value]

            elif buildBase and worker.point == buildBase and len(bases) > 0:
                sys.stderr.write("{}, {}\n".format(buildBase.x, buildBase.y))
                d = UnitType.BASE.value
                self.aStage.resourceNum -= Cost[UnitType.BASE.value]
                buildBase = None

            else:
                self.checkPoint(worker)
                if not worker.goal:
                    self.aStage.nearestResouce(worker)
                d = worker.goToPoint(worker.goal[0])

            if d:
                self.actions[worker.cid] = d

    def checkPoint(self, character):
        if not character.isFix and character.goal and character.goal[0] == character.point:
            character.goal.pop(0)

    def distToVillage(self, character):
        d = INF
        for v in self.aStage.supporter.unit[UnitType.CASTLE] + self.aStage.supporter.unit[UnitType.VILLAGE]:
            d = min(d, character.point.dist(v.point))
        return d

    def safetyVillage(self):
        strength = INF
        villange = None
        for v in self.aStage.supporter.unit[UnitType.VILLAGE]:
            s = self.aStage.enemies.aroundStrength(v.point, 10)
            if s < strength:
                strength = s
                villange = v
        if villange:
            return villange.point
        return None







