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
    for i in xrange(N):
        cid, y, x, hp, utype = map(int, raw_input().split())
        unitsId.append(cid)
        if cid in units:
            c = units[cid]
            c.point = Point(x, y)
            c.turn = turnNum
        else:
            units[cid] = Character(cid, y, x, hp, UnitType(utype), turnNum)

    # 永眠キャラを除去
    for key, unit in units.items():
        if key not in unitsId:
            units.pop(key)


    enemies = aBrain.aStage.enemies.units
    M = int(raw_input())
    for i in xrange(M):
        cid, y, x, hp, utype = map(int, raw_input().split())
        if cid in enemies:
            c = enemies[cid]
            c.point = Point(x, y)
            c.turn = turnNum
        enemies[cid] = Character(cid, y, x, hp, UnitType(utype), turnNum)

    R = int(raw_input())
    for i in xrange(R):
        y, x = map(int, raw_input().split())
        aBrain.aStage.updateResource(Point(x, y))
    aBrain.startTurn()
    raw_input()  # end


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
        turnInput(aBrain, time, stageNum)
        # except Exception as e:
        # pass
        print len(aBrain.actions)
        for k, v in aBrain.actions.items():
            print k, v


if __name__ == '__main__':
    print 'cocodrips'
    main()