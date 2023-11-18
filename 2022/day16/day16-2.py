import re

patt = R"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)"

def parse(filename):
    global flows, edges, max_flow
    flows = {}
    edges = {}

    with open(filename) as f:
        for line in f:
            m = re.match(patt, line)

            valve,flow,links = (s.strip() for s in m.groups())

            valve = valve.strip()
            flows[valve] = int(flow)
            edges[valve] = []

            for link in links.split(","):
                edges[valve].append(link.strip())

    max_flow = sum(v for _,v in flows)

    
def search1(turn, pos, valves, memo = {}):
    if turn >= 30:
        return 0

    memo_key = (turn, pos, tuple(sorted(valves.items())))

    if memo_key in memo:
        return memo[memo_key]

    scores = []

    turn_score = sum(flows[v] for v in valves.keys() if valves[v])

    if flows[pos] > 0:
        oldv = valves[pos]
        valves[pos] = True
        stay_score = search1(turn+1, pos, valves, memo)
        valves[pos] = oldv

        scores.append(turn_score + stay_score)

    for connection in edges[pos]:
        scores.append(turn_score + search1(turn+1, connection, valves, memo))

    ret = max(scores)
    memo[memo_key] = ret

    return ret

def search2(turn, pos, elph, valves, high_score = 0, memo = {}):
    if turn >= 26:
        return 0

    memo_key1 = (turn, pos, elph, tuple(v for _,v in sorted(valves.items())))
    memo_key2 = (turn, elph, pos, tuple(v for _,v in sorted(valves.items())))

    if memo_key1 in memo:
        return memo[memo_key1]
    if memo_key2 in memo:
        return memo[memo_key2]

    scores = []

    all_open = all(v for k,v in valves.items() if flows[k] > 0)
    turn_score = sum(flows[v] for v in valves.keys() if valves[v])

    if all_open:
        return (26 - turn) * turn_score

    

    opt1 = [pos] + edges[pos]
    opt2 = [elph] + edges[elph]

    scores = []

    for newpos,newelph in ((p1,p2) for p1 in opt1 for p2 in opt2):
        if newpos == pos and flows[pos] == 0:
            continue
        if newelph == elph and flows[elph] == 0:
            continue

        if turn < 15:
            print(" " * turn, newpos,newelph)

        oldp = valves[newpos]
        olde = valves[newelph]

        if newpos == pos:
            valves[pos] = True
        if newelph == elph:
            valves[elph] = True

        new_score = scores.append(
            turn_score + search2(turn+1, newpos, newelph, valves, high_score, memo))

        high_score = max(high_score, new_score)

        valves[newpos] = oldp
        valves[newelph] = olde

    ret = max(scores)
    memo[memo_key1] = ret
    return ret
    

parse("input.txt")
#parse("test.txt")
#print(tuple(sorted({1: 2, 3: 4}.items())))
print(search2(0, 'AA', 'AA', {v: False for v in flows.keys()}))
