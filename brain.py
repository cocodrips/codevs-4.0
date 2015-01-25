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
        self.bet = [Point(i, i) for i in xrange(31, MAPSIZE, 9)]
        self.pioneerMap = []

        for i in xrange(4, MAPSIZE, 9):
            for j in xrange(4, MAPSIZE, 9):
                if i == 0:
                    self.pioneerMap.insert(0, Point(i, j))
                elif i == j and 22 < i <= 76:
                    continue
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
        self.defenceMode = self.aStage.enemies.aroundStrength(self.castle.point,
                                                              Range[UnitType.CASTLE]) > DEFENCE_THRESHOLD
        # print >> sys.stderr, self.isAttack, self.aStage.turnNum, len(self.pioneerMap)
        # 順番考える
        self.work()
        self.product()
        self.base()
        self.force()

    ###############################################
    def unit(self, unitType):
        return self.aStage.supporter.unit[unitType]

    def enemyUnit(self, unitType):
        return self.aStage.enemies.unit[unitType]

    def forceUnit(self, units, forceType):
        return [unit for unit in units if unit.forceType == forceType]

    def damage(self, p):
        return self.aStage.enemies.damage(p)

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
    def enemyCastle(self):
        c = self.aStage.enemies.unit[UnitType.CASTLE]
        if c:
            return c[0]
        return None

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

        def canWait(self):
            if self.aStage.turnNum == 5:
                return True
            if self.aStage.turnNum < KEEP_WORKER:
                return False
            if len(self.forceUnit(self.unit(UnitType.WORKER), ForceType.GATEKEEPER)) > 1:
                return False
            if self.unit(UnitType.BASE) > 1:
                return False
            return True

        productions = self.productions[:]

        if canWait(self):
            if generate(self, self.castle):
                print >> sys.stderr, "城待機"
                productions.remove(self.castle)

        emptyResources = self.aStage.emptyResources()
        canGenerateProductions = set()
        for r in emptyResources:
            if distToUnits(r.point, productions) < PRODUCTION_INTERVAL:
                canGenerateProductions.add(closestUnit(r.point, productions))

        for p in canGenerateProductions:
            generate(self, p)


    def base(self):
        for base in self.aStage.supporter.unit[UnitType.BASE]:
            if self.defenceMode:
                if self.aStage.resourceNum < Cost[UnitType.FIGHTER.value]:
                    return
                if self.aStage.resourceNum >= Cost[UnitType.ASSASSIN.value]:
                    t = UnitType.FIGHTER.value +random.randint(0, 1)
                else:
                    t = UnitType.FIGHTER.value
                self.actions[base.cid] = t
                self.aStage.resourceNum -= Cost[t]
                continue

            if not self.enemyCastle:
                if self.aStage.resourceNum < Cost[UnitType.KNIGHT.value]:
                    return
                if self.aStage.resourceNum >= Cost[UnitType.ASSASSIN.value] and self.aStage.five:
                    t = UnitType.FIGHTER.value
                else:
                    if self.aStage.resourceNum >= Cost[UnitType.ASSASSIN.value]:
                        t = UnitType.ASSASSIN.value
                    else:
                        t = UnitType.KNIGHT.value + random.randint(0, 1)
                self.actions[base.cid] = t
                self.aStage.resourceNum -= Cost[t]
                continue

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
            for resource in self.resources:
                if resource.mother and not self.aStage.supporter.units.get(resource.mother.cid):
                    resource.mother = None
                if not resource.mother: #and self.aStage.enemies.aroundStrength(resource.point, 5) > 500:
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
            # point = p
            return force.goToPoint(point)

        def walker(self, force):
            point, strength = self.aStage.enemies.strongest(force.point, MAPSIZE)
            return force.goToPoint(point)

        resources = unsafetyResource(self)
        units = self.aStage.supporter.unit
        forces = units[UnitType.ASSASSIN] + units[UnitType.FIGHTER] + units[UnitType.KNIGHT]
        if not self.aStage.supporter.unit[UnitType.BASE]:
            return

        for force in forces:
            if force.forceType == ForceType.NEET:
                if force.type == UnitType.ASSASSIN and resources:
                    force.forceType = ForceType.HOUSE_SITTING
                elif force.type == UnitType.KNIGHT and len(self.forceUnit(self.unit(UnitType.KNIGHT),
                                                                          ForceType.GATEKEEPER)) < GATEKEEPERS:
                    force.forceType = ForceType.GATEKEEPER
                else:
                    if not self.enemyCastle and not self.defenceMode and len(forces) < FORCE_EXPLORER_NUM:
                        force.forceType = ForceType.CASTLE_EXPLORER
                    if self.aStage.turnNum % GROUP_INTERVAL == 0:

                        if self.aStage.supporter.aroundStrength(self.castle.point, DEFENCE_RANGE) < self.aStage.enemies.aroundStrength(self.castle.point, DEFENCE_RANGE):
                            force.forceType = ForceType.GATEKEEPER
                        else:
                            force.forceType = ForceType.ATTACKER
                        force.rightRate = int(self.aStage.turnNum % (GROUP_INTERVAL * 2) == 0)


            # 命令の種類
            d = None
            # 役割の決まった兵士たちの行動

            # GATEKEEPER
            if force.forceType == ForceType.GATEKEEPER:
                d = gatekeeper(self, force)

            if force.forceType == ForceType.HOUSE_SITTING:
                d = houseSitting(self, force)

            if force.forceType == ForceType.WALKER:
                d = walker(self, force)

            if force.forceType == ForceType.ATTACKER or force.forceType == ForceType.CASTLE_EXPLORER:
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
            elif len(workers) > 30:
                pioneerNum = 3

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
                worker.goal = self.bet
                self.bet = []
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
                    else:
                        # on resource
                        if len(self.unit(ForceType.WORKER)) < INCOME and distToUnits(worker.point,
                                                                                     self.productions) >= PRODUCTION_INTERVAL:
                            self.actions[worker.cid] = UnitType.VILLAGE.value
                            self.aStage.resourceNum -= Cost[UnitType.VILLAGE.value]
                        resource.workers.append(worker)

            for worker in fWorkers:
                if worker not in used and distToUnits(worker.point, self.resources) != 0:
                    d = worker.goToPoint(Point(MAPSIZE - 1, MAPSIZE - 1))
                    if d:
                        self.actions[worker.cid] = d

        def actBuilder(self, worker):
            d = worker.goToPoint(worker.goal[0])
            if d:
                self.actions[worker.cid] = d

        def buildBase(self, workers):
            halfStrength = self.aStage.enemies.rangeStrength(self.castle.point, Point(SILBER_POINT, SILBER_POINT))
            print >> sys.stderr, "strength:", halfStrength, self.aStage.five
            if self.aStage.isStartEnemyAttack and len(self.unit(UnitType.BASE)) < 1 and self.aStage.five:
                worker = min(workers, key=lambda x: x.point.dist(self.castle.point))
            else:
                zero = Point(60, 60)
                worker = min(workers, key=lambda x: x.point.dist(zero))

            self.actions[worker.cid] = UnitType.BASE.value
            self.aStage.resourceNum -= Cost[UnitType.BASE]
            workers.remove(worker)

        def canBuild(self):
            # lila
            if not self.isAttack:
                return False
            if self.aStage.resourceNum < Cost[UnitType.BASE] + 200 * int(self.aStage.five):
                return False
            if len(self.unit(UnitType.BASE)) > 1 and self.aStage.resourceNum < Cost[UnitType.BASE] * 2:
                return False
            return True

        def selectGatekeeper(self, workers):
            if self.aStage.turnNum > KEEP_WORKER and len(self.forceUnit(self.unit(UnitType.WORKER),
                                                                    ForceType.GATEKEEPER)) < 1:
                for worker in workers:
                    if worker.point == self.castle.point:
                        worker.forceType = ForceType.GATEKEEPER
                        break


        # worker 初期化
        workers = self.unit(UnitType.WORKER)[:]
        for worker in workers:
            turnStart(self, worker)

        if len(self.forceUnit(workers, ForceType.BASE_BUILDER)):
            worker = max(workers, key=lambda x: x.dist(MAPSIZE, MAPSIZE))
            worker.forceType = ForceType.BASE_BUILDER
            worker.goal.append(MAPSIZE - 1, MAPSIZE - 1)

        # 城に待機する人
        selectGatekeeper(self, workers)

        # Builder
        builder = self.forceUnit(workers, ForceType.BASE_BUILDER)
        if builder:
            actBuilder(self, builder[0])

        # 基地を建てる
        if canBuild(self):
            buildBase(self, workers)

        builder = self.forceUnit(workers, ForceType.GATEKEEPER)
        if builder:
            workers.remove(builder[0])

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
