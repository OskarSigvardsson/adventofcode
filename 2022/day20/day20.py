def load(filename):
    with open(filename) as f:
        ns = [int(line) for line in f]

    return ns

def sgn(n):
    if n == 0:
        return 0
    elif n > 0:
        return 1
    else:
        return -1

def part1(ns):
    nsc = ns[:]
    l = len(nsc)
    reorg = list(range(l))
    
    def swap(i1,i2):
        # if i1%l == 0 and i2%l == -1%l:
        #     reorg.append(reorg[0])
        #     del reorg[0]
        #     i1 -= 1
        #     i2 -= 1

        tmp = reorg[i1 % l]
        reorg[i1 % l] = reorg[i2 % l]
        reorg[i2 % l] = tmp

    print(0, [ns[k] for k in reorg])
    for i in range(len(ns)):
        k = reorg[i]
        n = ns[i]
        s = sgn(n)
        print("reorg", reorg)
        print(f"move {ns[i]} from index {k} {ns[i]} steps")

        if n == 0: continue

        for j in range(k, k+n, s):
            swap(j, j+s)

        print(i+1, [ns[k] for k in reorg])

    return nsc

print(part1(load("test.txt")))
