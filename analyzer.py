import collections
import re

with open('result/result5.txt', 'r') as r:
    p = re.compile("stage (\d+) \(vs (.*)\) : result=(.+)  score.* turn=(.*) ")
    d = collections.defaultdict(list)
    for line in r:
        g = p.match(line)
        if g:
            num, name, isWin, turn = g.groups()
            if int(num) < 27:
                d[name].append((num, isWin, turn))
            elif 27 <= int(num) < 34:
                d[name + " - 20"].append((num, isWin, turn))
            else:
                d[name + " -  30"].append((num, isWin, turn))

    for k, v in sorted(d.items()):
        print k
        win = 0
        for vv in v:
            print " ", ' '.join(vv)
            if vv[1] == 'win':
                win += 1
        print win, '/', len(v), (1.0 * win / len(v)) * 100
        print



