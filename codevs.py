# -*- coding: utf-8 -*-

import enum
import copy


class UnitType(enum.IntEnum):
    WORKER = 0
    KNIGHT = 1
    FIGHTER = 2
    ASSASSIN = 3
    CASTLE = 4
    VILLAGE = 5
    BASE = 6


class ForceType(enum.IntEnum):
    GATEKEEPER = 0
    WALKER = 1
    ATTACKER = 2
    HOUSE_SITTING = 3
    EXPLORER = 4
    PIONEER = 5
    WORKER = 6
    BASE_BUILDER = 7
    NEET = 8
    CASTLE_EXPLORER = 9
    GRUNRUN = 10

class F(enum.IntEnum):
    UNKNOWN = 0,
    TRUE = 1,
    FALSE = 2

class AI(enum.IntEnum):
    rosa = 0,
    colun = 1,
    zinnober = 2,
    gelb = 3,
    silber = 4,
    chokudai = 5,
    schwarz = 6,
    grun = 7,
    lila = 8,
    unknown = 9




FORGET_SET = set([UnitType.WORKER, UnitType.KNIGHT, UnitType.FIGHTER, UnitType.ASSASSIN])

Weak = [0, UnitType.FIGHTER, UnitType.ASSASSIN, UnitType.KNIGHT]
Cost = [40, 20, 40, 60, 0, 100, 500]
Range = [4, 4, 4, 4, 10, 10, 4]
AttackRange = [2, 2, 2, 2, 10, 2, 2]
Strength = [100, 200, 500, 1000, 100, 100, 100]
INF = 100000000
MAPSIZE = 100

# 町をどれくらいの間隔で作るか
PRODUCTION_INTERVAL = 40
INCOME = 25

GATEKEEPERS = 5
GROUP_INTERVAL = 10


# PIONEER_NUM
PIONEER_NUM = 5
KEEP_WORKER = 40

# 銀対策
SILBER_POINT = 65

# 防御
DEFENCE_THRESHOLD = 1500
FORCE_EXPLORER_NUM = 40
DEFENCE_RANGE = 60
GATEKEEP_STRENGTH = 200
WORKER_PRODUCTION_DAMAGE = 400

# Distance
def distToUnits(point, targets):
    """
    あるユニット(複数)への距離
    args: character, characters
    return: 距離(int)
    """
    if not targets or not point:
        return INF
    return min([point.dist(target.point) for target in targets])


def closestUnit(point, targets):
    """
    あるユニット(複数)への距離が１番近いやつ
    args: character, characters
    return: オブジェクト(Character)
    """
    if not targets or not point:
        return None
    return min(targets, key=lambda target: point.dist(target.point))

