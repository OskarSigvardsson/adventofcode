import subprocess

from collections import deque, defaultdict

verts = set()
edges = defaultdict(list)
edgeset = set()

with open("../inputs/day25-real.txt", "r") as f:
    lines = (line.split(":") for line in f)
    lines = [(c1, tuple(c2s.strip().split(" "))) for c1,c2s in lines]

    for c1,c2s in lines:
        verts.add(c1)

        for c2 in c2s:
            verts.add(c2)
            edges[c1].append(c2)
            edges[c2].append(c1)

            edgeset.add(tuple(sorted((c1,c2))))

def generate_graphviz(out):
    with open(out, "w") as f:
        with subprocess.Popen(["neato", "-T", "png"], stdin = subprocess.PIPE, stdout = f) as p:
            p.stdin.write(b"graph {\n")

            for v1,v2 in edgeset:
                p.stdin.write(f"    {v1} -- {v2}\n".encode())

            p.stdin.write(b"}\n")
            p.stdin.close()

def bfs(src):
    visited = set()
    frontier = deque()
    prev = {}
    last = None

    frontier.append((0, src,None))

    while len(frontier) > 0:
        #print(frontier)
        dist,v1,vprev = frontier.popleft()

        if v1 in visited:
            continue

        visited.add(v1)
        prev[v1] = vprev
        last = v1
        
        for v2 in edges[v1]:
            frontier.append((dist+1,v2,v1))

    return visited

# this generates a graphviz visualization which makes the solution BLINDINGLY obvious :) 
generate_graphviz("before.png")

def delete_edge(a, b):
    edges[a].remove(b)
    edges[b].remove(a)
    edgeset.remove(tuple(sorted((a,b))))
    
# this is disgusting!
delete_edge("krx", "lmg")
delete_edge("tqn", "tvf")
delete_edge("tnr", "vzb")

generate_graphviz("after.png")

print(len(bfs("krx")) * len(bfs("lmg")))
