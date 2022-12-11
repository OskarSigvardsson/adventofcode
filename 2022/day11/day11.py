import re

def input(f):
    items = []
    monkeys = []

    with open(f) as f:
        lines = f.readlines()
        i = 0

        while i < len(lines):
            monkey = int(re.match(R"Monkey (\d+):", lines[i]).group(1))
            i+=1
            assert(monkey == len(monkeys))

            its = eval("[" + re.match(R"  Starting items: (.*)", lines[i]).group(1) + "]")
            i+=1
            items.append(its)

            l,op,r = re.match(R"  Operation: new = (.*) (.) (.*)", lines[i]).groups()
            i+=1

            if l != "old":
                l = int(l)
            if r != "old":
                r = int(r)

            test = int(re.match(R"  Test: divisible by (\d+)", lines[i]).group(1))
            i+=1

            iftrue = int(re.match(R"    If true: throw to monkey (\d+)", lines[i]).group(1))
            i+=1
            iffalse = int(re.match(R"    If false: throw to monkey (\d+)", lines[i]).group(1))
            i+=1

            monkeys.append(((l,op,r), test, iftrue, iffalse))
            i+=1

    return items, monkeys


def solve(f, rounds, divisor):
    items, monkeys = input(f)
    inspected = [0] * len(monkeys)
    m = 1

    for _,test,_,_ in monkeys:
        m *= test

    for _ in range(rounds):
        for i in range(len(monkeys)):
            its = items[i]
            oper,test,iftrue,iffalse = monkeys[i]
            l,op,r = oper

            while len(its) > 0:
                inspected[i] += 1
                it = its.pop(0)

                lv = it if l == "old" else l
                rv = it if r == "old" else r

                if op == "*":
                    it = lv * rv
                elif op == "+":
                    it = lv + rv
                else:
                    assert(false)

                it = it // divisor

                it = it % m;

                if it % test == 0:
                    items[iftrue].append(it)
                else:
                    items[iffalse].append(it)

    inspected.sort()
    return inspected[-2] * inspected[-1]

print(solve("test.txt", 20, 3))
print(solve("input.txt", 20, 3))
print(solve("test.txt", 10000, 1))
print(solve("input.txt", 10000, 1))
