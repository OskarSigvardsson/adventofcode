from collections import defaultdict

import re

def part1(p1, p2):
    die = 100
    rolls = 0

    def roll():
        nonlocal die, rolls
        die = die % 100 + 1
        rolls += 1
        return die

    s1, s2 = 0, 0
    p1 -= 1
    p2 -= 1

    while s1 < 1000 and s2 < 1000:
        p1 = (p1 + roll() + roll() + roll()) % 10
        s1 += p1 + 1

        if s1 >= 1000: break

        p2 = (p2 + roll() + roll() + roll()) % 10
        s2 += p2 + 1

    return rolls * min(s1, s2)

def part2(p0, p1):
    def roll(die, p, s):
        p += die
        while p > 10: p -= 10
        s += p
        return p,s
    
    # advances the state a single step (with the turn parameter indicating who's
    # turn it is to roll). a bit of duplication here, but whatever
    def advance(state, turn):
        p0, s0, p1, s1 = state

        if turn == 0:
            p03,s03 = roll(3, p0, s0)
            p04,s04 = roll(4, p0, s0)
            p05,s05 = roll(5, p0, s0)
            p06,s06 = roll(6, p0, s0)
            p07,s07 = roll(7, p0, s0)
            p08,s08 = roll(8, p0, s0)
            p09,s09 = roll(9, p0, s0)

            # calculated this distribution BY HAND (by expanding the trinomial)
            # like it was the 1920s or something. i suffer for my art
            return {
                (p03,s03,p1,s1): 1,
                (p04,s04,p1,s1): 3,
                (p05,s05,p1,s1): 6,
                (p06,s06,p1,s1): 7,
                (p07,s07,p1,s1): 6,
                (p08,s08,p1,s1): 3,
                (p09,s09,p1,s1): 1
            }
        else:
            p13,s13 = roll(3, p1, s1)
            p14,s14 = roll(4, p1, s1)
            p15,s15 = roll(5, p1, s1)
            p16,s16 = roll(6, p1, s1)
            p17,s17 = roll(7, p1, s1)
            p18,s18 = roll(8, p1, s1)
            p19,s19 = roll(9, p1, s1)

            return {
                (p0,s0,p13,s13): 1,
                (p0,s0,p14,s14): 3,
                (p0,s0,p15,s15): 6,
                (p0,s0,p16,s16): 7,
                (p0,s0,p17,s17): 6,
                (p0,s0,p18,s18): 3,
                (p0,s0,p19,s19): 1
            }
            
        
    # this map counts the number of universes for a given state. the state is
    # four values, player 1 position and score, player 2 position and score
    universes = { (p0, 0, p1, 0): 1 }
    turn = 0

    p1wins = 0
    p2wins = 0
    
    while len(universes) > 0:
        newuniverses = defaultdict(lambda: 0)

        for universe,c_old in universes.items():
            for state,c_new in advance(universe, turn).items():
                p0,s0,p1,s1 = state
                count = c_old * c_new

                if s0 >= 21:
                    p1wins += count
                elif s1 >= 21:
                    p2wins += count
                else:
                    newuniverses[state] += count

        universes = newuniverses
        turn = 1 - turn

    return max(p1wins,p2wins)
        
    
with open("input.txt", "r") as f:
    p1 = int(re.match(R"Player 1 starting position: (\d+)", f.readline()).group(1))
    p2 = int(re.match(R"Player 2 starting position: (\d+)", f.readline()).group(1))

    print(f"Part 1: { part1(p1,p2) }")
    print(f"Part 2: { part2(p1,p2) }")
