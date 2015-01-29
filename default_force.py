# -*- coding: utf-8 -*-
from codevs import *
from model import Point
import sys


class DefaultForce(object):
    def __init__(self, brain):
        """
        :type brain: brain.Brain
        """
        self.brain = brain

    def neet(self, force, forces, resources):
        if resources and len(forces) > 10 and force.type == UnitType.ASSASSIN:
            force.forceType = ForceType.HOUSE_SITTING
        elif force.type == UnitType.KNIGHT and len(self.brain.forceUnit(self.brain.unit(UnitType.KNIGHT),
                                                                        ForceType.GATEKEEPER)) < GATEKEEPERS and len(
            forces) > 20:
            force.forceType = ForceType.GATEKEEPER
        else:
            if not self.brain.enemyCastle and not self.brain.defenceMode and len(forces) < FORCE_EXPLORER_NUM:
                force.forceType = ForceType.CASTLE_EXPLORER
            if self.brain.aStage.turnNum % GROUP_INTERVAL == 0:

                if int(self.brain.aStage.turnNum % (
                    GROUP_INTERVAL * 4) < 2) and self.brain.aStage.supporter.aroundStrength(
                    self.brain.castle.point, DEFENCE_RANGE) < self.brain.aStage.enemies.aroundStrength(
                    self.brain.castle.point,
                    DEFENCE_RANGE):
                    force.forceType = ForceType.GATEKEEPER
                else:
                    force.forceType = ForceType.ATTACKER
                force.rightRate = int(self.brain.aStage.turnNum % (GROUP_INTERVAL * 2) == 0)


    def check(self, character):
        if not character.isFix and character.goal and character.goal[0] == character.point:
            if self.brain.aStage.enemies.aroundStrength(character.point, Range[character.type.value]) < 200:
                character.goal.pop(0)


    def houseSitting(self, force, resources):
        # check(self, force)

        resources.sort(key=lambda x: x[0].point.dist(force.point))
        if not force.goal and resources:
            for r in resources:
                if not r[0].mother:
                    # if r[1] < Strength[force.type.value]:
                    r[0].mother.append(force)
                    # r[1] -= Strength[force.type.value]
                    force.goal.append(r[0].point)
                    break
                else:
                    resources.remove(r)

        d = ""
        if force.goal:
            d = force.goToPoint(force.goal[0])
        if not d:
            p, strength = self.brain.aStage.enemies.strongest(force.point, Range[force.forceType])
            if strength > GATEKEEP_STRENGTH:
                d = force.goToPoint(p)
        return d


    def gatekeeper(self, force):
        point = self.brain.castle.point
        p, strength = self.brain.aStage.enemies.strongest(point, Range[force.forceType])
        if strength > GATEKEEP_STRENGTH:
            point = p
        return force.goToPoint(point)


    def walker(self, force):
        point, strength = self.brain.aStage.enemies.strongest(force.point, MAPSIZE)
        return force.goToPoint(point)

    def unsafetyResource(self):
        r = []
        for resource in self.brain.resources:  # + self.aStage.enemies.unit[UnitType.VILLAGE]:
            resource.mother = [m for m in resource.mother if self.brain.aStage.supporter.units.get(m.cid)]
            if len(resource.mother) > 3:
                continue
            diff = sum([Strength[m.type.value] for m in resource.mother]) < self.brain.aStage.enemies.aroundStrength(
                resource.point, 5)
            if not resource.mother:  #and self.aStage.enemies.aroundStrength(resource.point, 5) > 400:
                r.append((resource, diff))

        return r