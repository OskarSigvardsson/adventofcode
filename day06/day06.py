import heapq

# this priority queue version is silly, but it's the first thing i thought of
# and it worked for day 1, so... the runtime is related to the number of fish,
# and the number of fish grows exponentially, so it only works for part 1
def part1(fish, days):
    fish = fish[:]
    heapq.heapify(fish)

    day = 0

    while fish[0] < days:
        day = heapq.heappop(fish)
        heapq.heappush(fish, day + 7)
        heapq.heappush(fish, day + 9)

    return len(fish)
    
# the way it works is you make a "schedule": a list of the days, and how many
# fish are born on that day. if X fish are born on day B, X more fish will be
# born on B + 9, B + 9 + 7, B + 9 + 2*7, etc. This algorithm is (I THINK) O(n^2)
# where n is the number of days, which is totally acceptible
def part2(fish, days):
    schedule = [0] * days

    for d in fish:
        while d < days:
            schedule[d] += 1
            d += 7

    total = len(fish)
    
    for day in range(days):
        born = schedule[day]
        total += born
        n = day + 9

        while n < days:
            schedule[n] += born
            n += 7

    return total
        
with open("input.txt", "r") as f:
    fish = [int(n) for n in f.readline().strip().split(",")]

    print(f"Part 1: { part1(fish, 80) }")
    print(f"Part 1: { part2(fish, 256) }")



