import enum


class UnitType(enum.IntEnum):
    WORKER = 0
    KNIGHT = 1
    FIGHTER = 2
    ASSASSIN = 3
    CASTLE = 4
    VILLAGE = 5
    BASE = 6


Cost = [40, 20, 40, 60, 0, 100, 500]
Range = [4, 4, 4, 4, 10, 10, 4]
AttackRange = [2, 2, 2, 2, 10, 2, 2]
Strength = [100, 100, 500, 1000, 100, 100, 100]
INF = 100000000
MAPSIZE = 100