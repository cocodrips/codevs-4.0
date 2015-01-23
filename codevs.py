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
    NEET = 7



Cost = [40, 20, 40, 60, 0, 100, 500]
Range = [4, 4, 4, 4, 10, 10, 4]
AttackRange = [2, 2, 2, 2, 10, 2, 2]
Strength = [100, 100, 500, 1000, 100, 100, 100]
INF = 100000000
MAPSIZE = 100

# 町をどれくらいの間隔で作るか
PRODUCTION_INTERVAL = 40
PIONEER_NUM = 8

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