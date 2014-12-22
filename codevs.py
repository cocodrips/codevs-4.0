import enum


class UnitType(enum.IntEnum):
    WORKER = 0
    KNIGHT = 1
    FIGHTER = 2
    ASSASSIN = 3
    CASTLE = 4
    VILLAGE = 5
    BASE = 6

Cost = [
    40,
    20,
    40,
    60,
    0,
    100,
    500
]

INF = 100000000