from codevs import *
from model import Character,Point
import brain

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

    aBrain.startTurn(time, stageNum, turnNum, units, enemies, resources)


def main():
    aBrain = brain.Brain()
    while True:
        turnInput(aBrain)


if __name__ == '__main__':
    print UnitType(0).value

