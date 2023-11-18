from itertools import cycle

with open("input.txt") as f:
    print(sum(int(line) for line in f));

with open("input.txt") as f:
    freq = 0;
    seen = set()

    for n in cycle(int(line) for line in f):
        freq += n
        
        if freq in seen:
            print(freq)
            break
        else:
            seen.add(freq)
