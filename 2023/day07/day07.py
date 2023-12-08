from collections import Counter

def score(hand):
    counts = sorted(Counter(hand).values())

    match counts:
        case [5]:         return 7
        case [1,4]:       return 6
        case [2,3]:       return 5
        case [1,1,3]:     return 4
        case [1,2,2]:     return 3
        case [1,1,1,2]:   return 2
        case [1,1,1,1,1]: return 1
    
    assert(false)
    
def joker_score(hand):
    return max(score(c if c > 0 else repl+1 for c in hand)
               for repl in range(len("23456789TQKA")))


    
with open("../inputs/day07-real.txt", "r") as f:
    strength = { c:i for i,c in enumerate("23456789TJQKA") }

    hands = [(tuple(strength[c] for c in hand), int(bid)) for hand,bid in (l.split(" ") for l in f)]

    scored = sorted((score(hand), hand, bid) for hand,bid in hands)
    result = sum(hand[2] * (rank + 1) for rank,hand in enumerate(scored))
    print(f"Part 1: {result}")


with open("../inputs/day07-real.txt", "r") as f:
    strength = { c:i for i,c in enumerate("J23456789TQKA") }

    hands = [(tuple(strength[c] for c in hand), int(bid)) for hand,bid in (l.split(" ") for l in f)]

    scored = sorted((joker_score(hand), hand, bid) for hand,bid in hands)
    result = sum(hand[2] * (rank + 1) for rank,hand in enumerate(scored))
    print(f"Part 2: {result}")
