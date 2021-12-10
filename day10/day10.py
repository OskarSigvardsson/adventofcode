
def parse(line):
    stack = []

    pairs = {
        "(": ")",
        "[": "]",
        "{": "}",
        "<": ">",
    }

    for c in line:
        if c in "({[<":
            stack.append(c)

        if c in ")}]>":
            popped = stack.pop()

            if c != pairs[popped]:
                return ("unexpected", c)

    # if we exit the loop with stuff still on the stack, it contains the
    # brackets we need in reverse order
    if len(stack) > 0:
        return ("expected", "".join(reversed([pairs[c] for c in stack])))

    return ("ok", ())

def part1(lines):
    points = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }

    return sum(points[c] for msg,c in (parse(line) for line in lines) if msg == "unexpected")

def part2(lines):
    points = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }

    tails = [tail for msg,tail in (parse(line) for line in lines) if msg == "expected"]

    def score(tail):
        score = 0

        # i much prefer traditional for loops to fold/reduce for aggregates :) 
        for c in tail:
            score = score * 5 + points[c]
        
        return score
    
    scores = sorted(score(tail) for tail in tails)

    return scores[len(scores)//2]

