# -*- coding: utf-8 -*-
from codevs import *
from model import Character, Point
import sys
import brain


def turnInput(aBrain, t, s):
    aBrain.aStage.time = t
    aBrain.aStage.stageNum = s
    aBrain.aStage.turnNum = int(raw_input())
    aBrain.aStage.resourceNum = int(raw_input())
    N = int(raw_input())

    turnNum = aBrain.aStage.turnNum
    units = aBrain.aStage.supporter.units
    unitsId = []
    isSecond = False
    for i in xrange(N):
        cid, y, x, hp, utype = map(int, raw_input().split())
        if utype == UnitType.CASTLE.value:
            if y >= 60:
                isSecond = True

        if isSecond:
            y = MAPSIZE - y
            x = MAPSIZE - x

        unitsId.append(cid)
        if cid in units:
            c = units[cid]
            c.point = Point(x, y)
            c.turn = turnNum
        else:
            units[cid] = Character(cid, y, x, hp, UnitType(utype), ForceType.NEET, turnNum)

    # 永眠キャラを除去
    for key, unit in units.items():
        if key not in unitsId:
            units.pop(key)

    aBrain.aStage.enemies.units = {k: v for k, v in aBrain.aStage.enemies.units.items() if v.type not in FORGET_SET}
    enemies = aBrain.aStage.enemies.units

    M = int(raw_input())
    for i in xrange(M):
        cid, y, x, hp, utype = map(int, raw_input().split())

        if isSecond:
            y = MAPSIZE - y
            x = MAPSIZE - x

        if cid in enemies:
            c = enemies[cid]
            c.point = Point(x, y)
            c.turn = turnNum
        enemies[cid] = Character(cid, y, x, hp, UnitType(utype), turnNum)

    R = int(raw_input())
    for i in xrange(R):
        y, x = map(int, raw_input().split())
        if isSecond:
            y = MAPSIZE - y
            x = MAPSIZE - x
        aBrain.aStage.updateResource(Point(x, y))
    aBrain.startTurn()
    raw_input()  # end
    return isSecond


def main():
    n = -1
    while True:
        sys.stdout.flush()
        time = int(raw_input())
        stageNum = int(raw_input())
        if stageNum != n:
            n = stageNum
            aBrain = brain.Brain()
        # try:
        isSecond = turnInput(aBrain, time, stageNum)
        # except Exception as e:
        # pass
        print len(aBrain.actions)
        for k, v in aBrain.actions.items():
            vv = v
            if isSecond:
                if v == 'U':
                    vv = 'D'
                elif v == 'D':
                    vv = 'U'
                elif v == 'R':
                    vv = 'L'
                elif v == 'L':
                    vv = 'R'

            print k, vv


if __name__ == '__main__':
    print 'cocodrips'
    main()