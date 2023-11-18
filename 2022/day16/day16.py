import re

from heapq import heappush,heappop

exit()
patt = R"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)"

def parse(filename):
    valves = []
    edges = {}
    flows = []

    with open(filename) as f:
        for line in f:
            m = re.match(patt, line)

            valve,flow,links = (s.strip() for s in m.groups())

            i = len(valves)
            valves.append(valve.strip())
            flows.append(int(flow))
            edges[i] = []

            for link in links.split(","):
                edges[i].append(link.strip())

    for links in edges.values():
        for i in range(len(links)):
            links[i] = valves.index(links[i])
            
    return valves, edges, flows

def search(valves, edges, flows):
    turns = 30
    perfect = (turns-1) * sum(flows)
    
    def score(state):
        turn,pos,valves = state

        return perfect - sum(t*f if t != 0 else (turns-turn)*f for (t,f) in zip(valves,flows))
        
    print("test score", perfect - score((0,0,[ 0,25, 6,28, 9, 0, 0,13, 0,21])))
                                            # AA,BB,CC,DD,EE,FF,GG,HH,II,JJ

    def neighbors(state):
        turn,pos,valves = state
        turn += 1

        nvs = list(valves)
        nvs[pos] = max(nvs[pos], turns - turn)
        nvs = tuple(nvs)

        yield (turn,pos,nvs)
        
        for nv in edges[pos]:
            yield (turn,nv,valves)

    
    init_state = (0,0,(0,)*len(valves))
    init_score = score(init_state)
    
    queue = [(init_score, init_state, None)]
    prevs = {}
    visited = set()
    
    i = 0
    
    while len(queue) > 0:
        scr,state,prev = heappop(queue)

        if state in visited:
            continue

        if i % 100000 == 0:
            print(i, len(queue), state[0])

        visited.add(state)
        prevs[state] = prev
        
        # print(scr,state)
        if state[0] == turns:
            print(state)
            ps = [(state, perfect - score(state))]
            while prevs[ps[-1][0]]:
                p = prevs[ps[-1][0]]
                ps.append((p, perfect - score(p)))
                
            return perfect - scr, reversed(ps)
        
        for ns in neighbors(state):
            turn,pos,vs = ns

            if turn == 30:
                print(perfect - score(vs))

            heappush(queue, (score(ns),ns,state))


valves,edges,flows = parse("input.txt")
score,prevs = search(valves, edges, flows)

print(score)
for p in prevs:
    print(p)
