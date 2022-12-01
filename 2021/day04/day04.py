

def bingo(board, numbers):
    marked = set()
    unmarked = set()
    tp = list(zip(*board))

    for row in board:
        unmarked.update(row)
    
    for n in numbers:
        marked.add(n)
        unmarked.discard(n)

        if any(all(n in marked for n in row) for row in board):
            return len(marked), n, unmarked

        if any(all(n in marked for n in row) for row in tp):
            return len(marked), n, unmarked
            
    return len(marked) + 1, -1, unmarked

def part1(boards, ns):
    boards = sorted(bingo(b, ns) for b in boards)
    marked, last, unmarked = boards[0]

    print(f"Part 1: { last * sum(unmarked) }")

def part2(boards, ns):
    boards = [bingo(b, ns) for b in boards]
    boards = sorted((m, l, u) for m,l,u in boards if l != -1)

    marked, last, unmarked = boards[len(boards) - 1]

    print(f"Part 2: { last * sum(unmarked) }")

with open("input.txt", "r") as f:
    lines = [line.strip() for line in f]
    ns = [int(n) for n in lines[0].split(",")]
    boards = [[[int(n) for n in line.split()]
               for line in lines[i:i+5]]
              for i in range(2, len(lines), 6)]

    part1(boards, ns)
    part2(boards, ns)
