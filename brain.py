# -*- coding: utf-8 -*-
from codevs import *
from model import Point
import stage
import random
import sys
import copy


class Brain():
    def __init__(self):
        self.aStage = stage.Stage()
        self.actions = []
        self.exp = []

    def startTurn(self):
        self.aStage.startTurn()
        self.actions = {}
        self.ai()

    def ai(self):
        # 順番考える
        self.work()
        self.product()
        # self.base()
        # self.force()

    ###############################################
    def unit(self, unitType):
        return self.aStage.supporter.unit[unitType]

    @property
    def castle(self):
        return self.aStage.supporter.unit[UnitType.CASTLE][0]

    ################################################


    def product(self):
        productions = copy.deepcopy(self.aStage.supporter.unit[UnitType.VILLAGE])
        # productions.sort(key=lambda x: (len(self.aStage.resources.get(x.point)),
        #                                 self.aStage.enemies.aroundStrength(x.point, 5)))  # ワーカーが少ない村に優先的に
        productions += self.aStage.supporter.unit[UnitType.CASTLE]
        resources = self.aStage.resources
        for resource, worker in resources.items():
            if not productions:
                return

            if len(worker) >= self.aStage.workerThrehold:
                continue

            if self.aStage.enemies.aroundStrength(resource, 5) > 1000:  # 危険度は調節
                continue

            for production in productions:
                if production.point.dist(resource) < 80 and self.aStage.enemies.aroundStrength(resource, 5) < 10000:
                    self.actions[production.cid] = UnitType.WORKER.value
                    self.aStage.resourceNum -= Cost[UnitType.WORKER.value]
                    productions.remove(production)

        c = self.aStage.supporter.unit[UnitType.CASTLE][0]
        # for production in productions:
        if self.aStage.enemies.aroundStrength(c.point, 5) > 10 \
            or (len(self.aStage.supporter.unit[UnitType.WORKER])) < 40 and len(self.aStage.supporter.unit[UnitType.BASE]) < 1:
            if self.aStage.resourceNum > 40:
                self.actions[c.cid] = UnitType.WORKER.value
                self.aStage.resourceNum -= 40


    def base(self):
        for base in self.aStage.supporter.unit[UnitType.BASE]:
            if self.aStage.resourceNum < Cost[UnitType.ASSASSIN.value]:
                return

            else:
                t = UnitType.KNIGHT.value + min(2, random.randint(0, 3))
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
        if not self.aStage.supporter.unit[UnitType.BASE]:
            return
        basePoint = self.aStage.supporter.unit[UnitType.BASE][0].point


        for force in forces:
            check(self, force)
            #生成された兵士はここで命を受ける
            if not force.forceType:
                # 城から生成される兵士
                if force.point == basePoint and self.aStage.turnNum % 10 != 0:
                    continue
                else:
                    if random.randint(0, 15) == 0:
                        force.forceType = 1
                    else:
                        force.forceType = 2

            # 命令の種類
            d = None
            # 役割の決まった兵士たちの行動

            # GATEKEEPER
            if force.forceType == ForceType.GATEKEEPER:
                point = castlePoint.plus(Point(5 * (force.cid % 5), 5 * (force.cid / 5 % 5) - 10))
                p, strength =  self.aStage.enemies.rangeStrength(force.point, 4)
                if strength > 1:
                    point = p
                d = force.goToPoint(point)

            # WALKER
            elif force.forceType == ForceType.WALKER:
                for resource in resources:
                    if force.point.dist(resource) < 15:
                        force.goal = [resource]
                        d = force.goToPoint(force.goal[0])
                        resources.remove(resource)
                        break
                if not d:
                    self.aStage.castlePoint(force)
                    d = force.goToPoint(force.goal[0])

            else:
                self.aStage.castlePoint(force)
                d = force.goToPoint(force.goal[0])

            if d:
                self.actions[force.cid] = d

    def work(self):
        bases = self.unit(UnitType.BASE)
        workers = self.unit(UnitType.WORKER)
        castlePoint = self.castle.point

        buildBase = None
        if Cost[UnitType.BASE.value] < self.aStage.resourceNum:
            buildBase = self.safetyVillage()
            if buildBase:
                sys.stderr.write("plan {},{}\n".format(buildBase.x, buildBase.y))

        basePoint = Point(0, 0)
        for worker in workers:
            if basePoint.x + basePoint.y < worker.point.x + worker.point.y:
                basePoint = worker.point

        strongest = self.aStage.enemies.strongest(castlePoint, 10)[0]

        for worker in workers:
            d = False
            # if worker.point in self.aStage.resources and self.aStage.resourceNum > Cost[
            #     UnitType.VILLAGE.value] and self.distToVillage(worker) > 50:
            #     d = UnitType.VILLAGE.value
            #     self.aStage.resourceNum -= Cost[UnitType.VILLAGE.value]

            if worker.forceType == ForceType.PIONEER and worker.point in self.aStage.resources and self.aStage.resourceNum > Cost[UnitType.VILLAGE.value] and self.distToVillage(worker) > 50:
                d = UnitType.VILLAGE.value
                self.aStage.resourceNum -= Cost[UnitType.VILLAGE.value]

            elif worker.point == basePoint and self.aStage.resourceNum > Cost[UnitType.BASE.value] and len(bases) < 1:
                d = UnitType.BASE.value
                self.aStage.resourceNum -= Cost[UnitType.BASE.value]

            elif buildBase and worker.point == buildBase and len(bases) > 0:
                sys.stderr.write("{}, {}\n".format(buildBase.x, buildBase.y))
                d = UnitType.BASE.value
                self.aStage.resourceNum -= Cost[UnitType.BASE.value]
                buildBase = None

            else:
                self.checkPoint(worker)
                if castlePoint.isRange(worker.point, 10) and self.aStage.enemies.aroundStrength(worker.point, 4) > 100:
                    d = worker.goToPoint(strongest)
                else:
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
        strength = 10000
        villange = None
        for v in self.aStage.supporter.unit[UnitType.VILLAGE]:
            s = self.aStage.enemies.aroundStrength(v.point, 10)
            if s < strength:
                strength = s
                villange = v
        if villange:
            return villange.point
        return None







