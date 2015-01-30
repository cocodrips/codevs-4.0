# -*- coding: utf-8 -*-
from codevs import *
from model import Point
import stage
import random
import sys
import copy
import random
import grun, lila, schwarz, five, silber
from default_worker import DefaultWorker
from default_force import DefaultForce
from default_product import DefaultProduct
from default_base import DefaultBase


class Brain():
    def __init__(self):
        self.aStage = stage.Stage()
        self.actions = []
        self.exp = []
        self.bet = [[Point(i, i) for i in xrange(31, MAPSIZE, 9)]]
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
        self.ai = self.judgeAI()

        print >> sys.stderr, self.aStage.turnNum, self.ai
        if self.ai == AI.grun:
            grun.order(self)
        elif self.ai == AI.lila:
            lila.order(self)
        elif self.ai == AI.schwarz:
            schwarz.order(self)
        elif self.ai == AI.silber:
            silber.order(self)
        else:
            if self.aStage.five:
                five.order(self)
            else:
                self.order()

    def judgeAI(self):
        if not self.aStage.five: # and not (self.aStage.is20 or self.aStage.is30): #本番のみ
            if self.aStage.isGrun == F.TRUE:
                return AI.grun
            if self.aStage.assasin == F.TRUE and self.aStage.hasVillage == F.UNKNOWN:
                return AI.schwarz
            if self.aStage.hasVillage == F.TRUE and self.aStage.isCastleBase != F.FALSE:
                return AI.lila
        else:
            if self.aStage.isSilber == F.TRUE:
                return AI.silber

        return AI.unknown


    def order(self):
        """
        それぞれのユニットの命令を呼び出す
        """
        self.isAttack = len(self.unit(UnitType.WORKER)) > INCOME
        self.defenceMode = self.aStage.enemies.aroundStrength(self.castle.point,
                                                              Range[UnitType.CASTLE]) > DEFENCE_THRESHOLD
        # print >> sys.stderr, self.isAttack, self.aStage.turnNum, len(self.pioneerMap)
        # 順番考える
        # print >> sys.stderr, self.aStage.turnNum, len(self.aStage.enemies.unit[UnitType.ASSASSIN]), len(self.aStage.enemies.unit[UnitType.KNIGHT])
        self.work(DefaultWorker(self))
        self.product(DefaultProduct(self))
        self.base(DefaultBase(self))
        self.force(DefaultForce(self))


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

    @property
    def weakType(self):
        return self.aStage.enemies.weakType

    @property
    def forces(self):
        return self.aStage.supporter.forces()


    ################################################


    def product(self, command):
        productions = self.productions[:]
        if command.canWait():
            if command.generate(self.castle):
                print >> sys.stderr, self.aStage.turnNum, "城待機"
                productions.remove(self.castle)

        emptyResources = self.aStage.emptyResources()
        canGenerateProductions = set()
        for r in emptyResources:
            if distToUnits(r.point, productions) < PRODUCTION_INTERVAL:
                canGenerateProductions.add(closestUnit(r.point, productions))

        for p in canGenerateProductions:
            command.generate(p)


    def base(self, command):
        for base in self.aStage.supporter.unit[UnitType.BASE]:
            if not self.enemyCastle:
                if command.noCastle(base):
                    continue

            if command.housesit(base):
                continue

            command.default(base)

    def force(self, command):
        resources = command.unsafetyResource()
        forces = self.forces

        for force in forces:
            if force.forceType == ForceType.NEET:
                command.neet(force, forces, resources)
            # 命令の種類
            d = None
            # 役割の決まった兵士たちの行動

            # GATEKEEPER
            if force.forceType == ForceType.GATEKEEPER:
                d = command.gatekeeper(force)

            if force.forceType == ForceType.HOUSE_SITTING:
                d = command.houseSitting(force, resources)

            if force.forceType == ForceType.WALKER:
                d = command.walker(force)

            if force.forceType == ForceType.ATTACKER or force.forceType == ForceType.CASTLE_EXPLORER:
                d = command.attack(force)

            if force.forceType == ForceType.EXPLORER:
                d = command.explorer(force)

            if d:
                self.actions[force.cid] = d

    def work(self, command):
        # worker 初期化
        workers = self.unit(UnitType.WORKER)[:]
        for worker in workers:
            command.turnStart(worker)

        if len(self.forceUnit(workers, ForceType.BASE_BUILDER)):
            worker = max(workers, key=lambda x: x.dist(MAPSIZE, MAPSIZE))
            worker.forceType = ForceType.BASE_BUILDER
            worker.goal.append(MAPSIZE - 1, MAPSIZE - 1)

        # 城に待機する人
        command.selectGatekeeper(workers)

        # Builder
        builder = self.forceUnit(workers, ForceType.BASE_BUILDER)
        if builder:
            command.actBuilder(builder[0])

        # 基地を建てる
        if command.canBuild():
            command.buildBase(workers)

        builder = self.forceUnit(workers, ForceType.GATEKEEPER)
        if builder:
            workers.remove(builder[0])

        # どれをPioneerか決める
        command.selectPioneer(workers)

        # Pioneerの行動
        pioneers = self.forceUnit(workers, ForceType.PIONEER)
        for pioneer in pioneers:
            command.actPioneer(pioneer)

        # ニートは強制ジョブチェンジ
        neets = self.forceUnit(workers, ForceType.NEET)
        for neet in neets:
            neet.forceType = ForceType.WORKER

        # 労働者の配分をする
        fWorkers = self.forceUnit(workers, ForceType.WORKER)
        command.actWorker(fWorkers)

    def checkPoint(self, character):
        if character.goal and character.goal[0] == character.point:
            character.goal.pop(0)
