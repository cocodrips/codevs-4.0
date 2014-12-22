from codevs import *
from model import Character,Point
import brain

NAME = "cocodrips"
def turnInput(aBrain):
    time = int(raw_input())
    stageNum = int(raw_input())
    turnNum = int(raw_input())
    resourceNum = int(raw_input())

    units = []
    N = int(raw_input())
    for i in xrange(N):
        cid, y, x, hp, utype = map(int, raw_input().split())
        units.append(Character(cid, y, x, hp, UnitType(utype)))

    enemies = []
    M = int(raw_input())
    for i in xrange(M):
        cid, y, x, hp, utype = map(int, raw_input().split())
        enemies.append(Character(cid, y, x, hp, UnitType(utype)))

    resources = []
    R = int(raw_input())
    for i in xrange(R):
        y, x = map(int, raw_input().split())
        resources.append(Point(x, y))
    aBrain.startTurn(time, stageNum, turnNum, resourceNum, units, enemies, resources)
    raw_input() #end

def main():
    aBrain = brain.Brain()
    while True:
        turnInput(aBrain)
        print NAME
        print len(aBrain.actions)
        for action in aBrain.actions:
            print action[0], action[1]

if __name__ == '__main__':
    main()