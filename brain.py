# -*- coding: utf-8 -*-
from codevs import *
from model import Point
import stage
import random
import sys
import copy
import random


class Brain():
    def __init__(self):
        self.aStage = stage.Stage()
        self.actions = []
        self.exp = []
        self.bet = [Point(MAPSIZE - 40, MAPSIZE - 40)]
        self.pioneerMap = []

        for i in xrange(4, MAPSIZE, 9):
            for j in xrange(4, MAPSIZE, 9):
                if i == 0:
                    self.pioneerMap.insert(0, Point(i, j))
                else:
                    self.pioneerMap.append(Point(i, j))


    def startTurn(self):
        self.aStage.startTurn()
        self.actions = {}
        self.ai()


    def ai(self):
        """
        それぞれのユニットの命令を呼び出す
        """
        self.isAttack = len(self.unit(UnitType.WORKER)) > INCOME
        # print >> sys.stderr, self.isAttack, self.aStage.turnNum, len(self.pioneerMap)
        # 順番考える
        self.work()
        self.product()
        self.base()
        self.force()

    ###############################################
    def unit(self, unitType):
        return self.aStage.supporter.unit[unitType]

    def forceUnit(self, units, forceType):
        return [unit for unit in units if unit.forceType == forceType]

    @property
    def productions(self):
        return self.unit(UnitType.CASTLE) + self.unit(UnitType.VILLAGE)

    @property
    def resources(self):
        return self.aStage.resources.values()

    @property
    def castle(self):
        return self.aStage.supporter.unit[UnitType.CASTLE][0]

    @property
    def isEnemy(self):
        return len(self.aStage.enemies.forces()) > 0
    ################################################


    def product(self):
        def generate(self, production):
            # 何度も呼ぶので無駄
            margin = len(self.unit(UnitType.BASE)) * Cost[UnitType.KNIGHT.value] + Cost[UnitType.WORKER.value]

            if self.aStage.resourceNum >= margin:
                self.aStage.resourceNum -= Cost[UnitType.WORKER.value]
                self.actions[production.cid] = UnitType.WORKER.value
                return True
            return False

        productions = self.productions[:]

        emptyResources = self.aStage.emptyResources()
        canGenerateProductions = set()
        for r in emptyResources:
            if distToUnits(r.point, productions) < PRODUCTION_INTERVAL:
                canGenerateProductions.add(closestUnit(r.point, productions))

        for p in canGenerateProductions:
            generate(self, p)




            # if self.pioneerGoal:
            # for p in (set(productions) - canGenerateProductions):
            # generate(self, p)



            # productions.sort(key=lambda x: (len(self.aStage.resources.get(x.point)),
            # self.aStage.enemies.aroundStrength(x.point, 5)))  # ワーカーが少ない村に優先的に

            # productions += self.aStage.supporter.unit[UnitType.CASTLE]
            # resources = self.aStage.resources
            # for resource, worker in resources.items():
            # if not productions:
            #         return
            #
            #     if len(worker) >= self.aStage.workerThrehold:
            #         continue
            #
            #     if self.aStage.enemies.aroundStrength(resource, 5) > 1000:  # 危険度は調節
            #         continue
            #
            #     for production in productions:
            #         if production.point.dist(resource) < 80 and self.aStage.enemies.aroundStrength(resource, 5) < 10000:
            #             self.actions[production.cid] = UnitType.WORKER.value
            #             self.aStage.resourceNum -= Cost[UnitType.WORKER.value]
            #             productions.remove(production)
            #
            # c = self.aStage.supporter.unit[UnitType.CASTLE][0]
            # # for production in productions:
            # if self.aStage.enemies.aroundStrength(c.point, 5) > 10 \
            #     or (len(self.aStage.supporter.unit[UnitType.WORKER])) < 40 and len(self.aStage.supporter.unit[UnitType.BASE]) < 1:
            #     if self.aStage.resourceNum > 40:
            #         self.actions[c.cid] = UnitType.WORKER.value
            #         self.aStage.resourceNum -= 40


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
            for resource in self.resources:
                if resource.mother and not self.aStage.supporter.units.get(resource.mother.cid):
                    resource.mother = None
                if not resource.mother and self.aStage.enemies.aroundStrength(resource.point, 10) > 100:
                    r.append(resource)

            return r

        def houseSitting(self, force):
            if not force.goal and resources:
                # closest = closestUnit(resources)
                r = resources.pop()
                r.mother = force
                force.goal.append(r.point)

            if force.goal:
                return force.goToPoint(force.goal[0])

        def gatekeeper(self, force):
            point = self.castle.point
            # p, strength = self.aStage.enemies.rangeStrength(force.point, Point())
            # if strength > 1:
            #     point = p
            return force.goToPoint(point)

        resources = unsafetyResource(self)
        units = self.aStage.supporter.unit
        forces = units[UnitType.ASSASSIN] + units[UnitType.FIGHTER] + units[UnitType.KNIGHT]
        castlePoint = self.aStage.supporter.unit[UnitType.CASTLE][0].point
        if not self.aStage.supporter.unit[UnitType.BASE]:
            return
        basePoint = self.aStage.supporter.unit[UnitType.BASE][0].point

        for force in forces:
            if force.forceType == ForceType.NEET:
                if force.type == UnitType.ASSASSIN and resources:
                    force.forceType = ForceType.HOUSE_SITTING
                elif force.type == UnitType.KNIGHT and len(self.forceUnit(self.unit(UnitType.KNIGHT),
                                                                          ForceType.GATEKEEPER)) < GATEKEEPERS:
                    force.forceType = ForceType.GATEKEEPER
                else:
                    force.forceType = ForceType.ATTACKER


            # 命令の種類
            d = None
            # 役割の決まった兵士たちの行動

            # GATEKEEPER
            if force.forceType == ForceType.GATEKEEPER:
                d = gatekeeper(self, force)

            if force.forceType == ForceType.HOUSE_SITTING:
                d = houseSitting(self, force)

            if force.forceType == ForceType.ATTACKER:
                self.aStage.castlePoint(force)
                d = force.goToPoint(force.goal[0])

            if d:
                self.actions[force.cid] = d

    def work(self):
        def turnStart(self, worker):
            self.checkPoint(worker)
            if not worker.goal:
                worker.forceType = ForceType.WORKER
                return

        def selectPioneer(self, workers):
            pioneers = self.forceUnit(workers, ForceType.PIONEER)
            i = len(pioneers)
            table = pTable(self, workers)
            usedWorker, usedPoint = [], []
            pioneerNum = PIONEER_NUM
            if self.isAttack:
                pioneerNum = 1
            elif len(workers) > 10:
                pioneerNum = 2

            for dist, point, worker in table:
                if worker in usedWorker or point in usedPoint:
                    continue
                if i > pioneerNum:
                    break
                usedWorker.append(worker)
                usedPoint.append(point)
                self.pioneerMap.remove(point)
                worker.forceType = ForceType.PIONEER
                worker.goal.append(point)
                i += 1

        def actPioneer(self, worker):
            """
            PIONEER
                0. 目的地へ
                1. 目の前に他の家から40以上離れてる資源を見つけたらそこに家を建てる
            """

            cResource = closestUnit(worker.point, self.resources)
            # リソース <= 2 and 他の町 >= 40
            if cResource and cResource.point.dist(worker.point) <= Range[UnitType.WORKER] and distToUnits(
                cResource.point, self.productions) >= PRODUCTION_INTERVAL:
                # 他に資源に向かってる者がいない
                if len(cResource.volunteer) <= 0:
                    cResource.planners.append(worker)
                    worker.goal.insert(0, cResource.point)

            if self.bet:
                worker.goal.append(self.bet.pop())
                worker.rightRate = 0.5
                d = worker.goToPoint(worker.goal[0])
                if d:
                    self.actions[worker.cid] = d

            elif cResource and cResource.point == worker.point and distToUnits(worker.point,
                                                                               self.productions) >= PRODUCTION_INTERVAL:
                # 資源なかったらお留守番
                if self.aStage.resourceNum >= Range[UnitType.VILLAGE.value]:
                    self.actions[worker.cid] = UnitType.VILLAGE.value
                    self.aStage.resourceNum -= Cost[UnitType.VILLAGE.value]

            elif worker.goal:
                d = worker.goToPoint(worker.goal[0])
                if d:
                    self.actions[worker.cid] = d
            else:
                worker.forceType = ForceType.WORKER

        def pTable(self, workers):
            """
            未開地とworkersの距離をはかる
            """
            table = []
            for p in self.pioneerMap:
                for w in workers:
                    if w.forceType != ForceType.PIONEER:
                        d = w.point.dist(p)
                        table.append((d, p, w))

            table.sort()
            return table

        def rtTable(self, workers):
            """
            資源-ワーカ が近い順リストを作る
            """
            table = []
            for r in self.aStage.resources.values():
                for w in workers:
                    d = w.point.dist(r.point)
                    table.append((d, r, w))
            return sorted(table)

        def actWorker(self, fWorkers):
            """
            Workerの動きを決定する
            """
            table = rtTable(self, fWorkers)
            used = set()
            for dist, resource, worker in table:
                # 0: distance, 1:resource, 2:worker
                if worker not in used and len(resource.volunteer) < self.aStage.workerThrehold:
                    d = worker.goToPoint(resource.point)
                    used.add(worker)
                    if d:
                        self.actions[worker.cid] = d
                        resource.planners.append(worker)
                    else:  # on resource
                        if len(self.unit(ForceType.WORKER)) < INCOME and distToUnits(worker.point,
                                                                                     self.productions) >= PRODUCTION_INTERVAL:
                            self.actions[worker.cid] = UnitType.VILLAGE.value
                            self.aStage.resourceNum -= Cost[UnitType.VILLAGE.value]
                        resource.workers.append(worker)

        def buildBase(self, workers):
            zero = Point(MAPSIZE, MAPSIZE)
            worker = min(workers, key=lambda x: x.point.dist(zero))
            # for worker in workers:
            #     if worker.point == self.castle.point:
            self.actions[worker.cid] = UnitType.BASE.value
            self.aStage.resourceNum -= Cost[UnitType.BASE]
            workers.remove(worker)

        def isBuild(self):
            # if not (self.isAttack or self.isEnemy):
            #     return False
            if self.aStage.resourceNum < Cost[UnitType.BASE]:
                return False
            # if len(self.unit(UnitType.BASE)) < 1:
            return True

        # worker 初期化
        workers = self.unit(UnitType.WORKER)[:]
        for worker in workers:
            turnStart(self, worker)

        # 基地を建てる
        if isBuild(self):
            buildBase(self, workers)

        # どれをPioneerか決める
        selectPioneer(self, workers)

        # Pioneerの行動
        pioneers = self.forceUnit(workers, ForceType.PIONEER)
        for pioneer in pioneers:
            actPioneer(self, pioneer)

        # ニートは強制ジョブチェンジ
        neets = self.forceUnit(workers, ForceType.NEET)
        for neet in neets:
            neet.forceType = ForceType.WORKER

        # 労働者の配分をする
        fWorkers = self.forceUnit(workers, ForceType.WORKER)
        actWorker(self, fWorkers)

    def checkPoint(self, character):
        if character.goal and character.goal[0] == character.point:
            character.goal.pop(0)
