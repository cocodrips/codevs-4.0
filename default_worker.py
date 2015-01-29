# -*- coding: utf-8 -*-
from codevs import *
from model import Point
import sys

class DefaultWorker(object):
    def __init__(self, brain):
        """
        :type brain: brain.Brain
        """
        self.brain = brain


    def turnStart(self, worker):
        self.brain.checkPoint(worker)
        if not worker.goal:
            worker.forceType = ForceType.WORKER
            return

    def selectPioneer(self, workers):
        pioneers = self.brain.forceUnit(workers, ForceType.PIONEER)
        i = len(pioneers)
        table = self.pTable(workers)
        usedWorker, usedPoint = [], []
        pioneerNum = PIONEER_NUM
        if self.brain.isAttack:
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
            self.brain.pioneerMap.remove(point)
            worker.forceType = ForceType.PIONEER
            worker.goal.append(point)
            i += 1

    def actPioneer(self, worker):
        """
        PIONEER
            0. 目的地へ
            1. 目の前に他の家から40以上離れてる資源を見つけたらそこに家を建てる
        """

        cResource = closestUnit(worker.point, self.brain.resources)
        # リソース <= 2 and 他の町 >= 40
        if cResource and cResource.point.dist(worker.point) <= Range[UnitType.WORKER] and distToUnits(
            cResource.point, self.brain.productions) >= PRODUCTION_INTERVAL:
            # 他に資源に向かってる者がいない
            if len(cResource.volunteer) <= 0:
                cResource.planners.append(worker)
                worker.goal.insert(0, cResource.point)

        if self.brain.bet:
            worker.goal = self.brain.bet.pop()
            worker.rightRate = 0.5
            d = worker.goToPoint(worker.goal[0])
            if d:
                self.brain.actions[worker.cid] = d

        elif cResource and cResource.point == worker.point and distToUnits(worker.point,
                                                                           self.brain.productions) >= PRODUCTION_INTERVAL:
            # 資源なかったらお留守番
            if self.brain.aStage.resourceNum >= Range[UnitType.VILLAGE.value]:
                self.brain.actions[worker.cid] = UnitType.VILLAGE.value
                self.brain.aStage.resourceNum -= Cost[UnitType.VILLAGE.value]

        elif worker.goal:
            d = worker.goToPoint(worker.goal[0])
            if d:
                self.brain.actions[worker.cid] = d
        else:
            worker.forceType = ForceType.WORKER

    def pTable(self, workers):
        """
        未開地とworkersの距離をはかる
        """
        table = []
        for p in self.brain.pioneerMap:
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
        for r in self.brain.aStage.resources.values():
            for w in workers:
                d = w.point.dist(r.point)
                table.append((d, r, w))
        return sorted(table)

    def actWorker(self, fWorkers):
        """
        Workerの動きを決定する
        """
        table = self.rtTable(fWorkers)
        used = set()
        for dist, resource, worker in table:
            # 0: distance, 1:resource, 2:worker
            if worker not in used and len(resource.volunteer) < self.brain.aStage.workerThrehold:
                d = worker.goToPoint(resource.point)
                used.add(worker)
                if d:
                    self.brain.actions[worker.cid] = d
                    resource.planners.append(worker)
                else:
                    # on resource
                    if len(self.brain.unit(ForceType.WORKER)) < INCOME and distToUnits(worker.point,
                                                                                 self.brain.productions) >= PRODUCTION_INTERVAL and self.brain.aStage.enemies.aroundStrength(worker.point, 6) < 1000:
                        self.brain.actions[worker.cid] = UnitType.VILLAGE.value
                        self.brain.aStage.resourceNum -= Cost[UnitType.VILLAGE.value]
                    resource.workers.append(worker)

        for worker in fWorkers:
            if worker not in used and distToUnits(worker.point, self.brain.resources) != 0:
                d = worker.goToPoint(self.brain.aStage.enemies.strongest(worker.point, 5)[0])
                if d:
                    self.brain.actions[worker.cid] = d

    def actBuilder(self, worker):
        d = worker.goToPoint(worker.goal[0])
        if d:
            self.brain.actions[worker.cid] = d

    def buildBase(self, workers):
        halfStrength = self.brain.aStage.enemies.rangeStrength(self.brain.castle.point, Point(SILBER_POINT, SILBER_POINT))
        print >> sys.stderr, "strength:", halfStrength, self.brain.aStage.five
        if self.brain.aStage.isStartEnemyAttack and len(self.brain.unit(UnitType.BASE)) < 1 and self.brain.aStage.five:
            worker = min(workers, key=lambda x: x.point.dist(self.brain.castle.point))
        else:
            zero = Point(60, 60)
            worker = min(workers, key=lambda x: x.point.dist(zero))

        self.brain.actions[worker.cid] = UnitType.BASE.value
        self.brain.aStage.resourceNum -= Cost[UnitType.BASE]
        workers.remove(worker)

    def canBuild(self):
        # lila
        if not self.brain.isAttack:
            return False
        if self.brain.aStage.resourceNum < Cost[UnitType.BASE] + 200 * int(self.brain.aStage.five):
            return False
        if len(self.brain.unit(UnitType.BASE)) > 0 and self.brain.aStage.resourceNum < Cost[UnitType.BASE.value] * 2:
            return False
        return True

    def selectGatekeeper(self, workers):
        if self.brain.aStage.turnNum > KEEP_WORKER and len(self.brain.forceUnit(self.brain.unit(UnitType.WORKER),
                                                                    ForceType.GATEKEEPER)) < 1:
            for worker in workers:
                if worker.point == self.brain.castle.point:
                    worker.forceType = ForceType.GATEKEEPER
                    break
