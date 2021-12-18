from itertools import product
from math import floor, ceil

class Node:
    parent = None
    val = None
    c1 = None
    c2 = None

    def __init__(self, lst, parent = None):
        self.parent = parent

        if isinstance(lst, int):
            self.val = lst
        else:
            self.c1 = Node(lst[0], self)
            self.c2 = Node(lst[1], self)

    def __str__(self):
        if self.val is not None:
            return str(self.val)
        return f"[{str(self.c1)}, {str(self.c2)}]"
    
    def first(self):
        if self.val is not None:
            return self

        return self.c1.first()

    def last(self):
        if self.val is not None:
            return self

        return self.c2.last()
    
    def pred(self):
        curr = self

        while curr.parent is not None:
            if curr == curr.parent.c2:
                return curr.parent.c1.last()
            curr = curr.parent
            
    def succ(self):
        curr = self

        while curr.parent is not None:
            if curr == curr.parent.c1:
                return curr.parent.c2.first()
            curr = curr.parent

    def explode(self, level=4):
        if self.val is not None:
            return

        if level == 0:
            pred = self.pred()
            succ = self.succ()
            
            if pred: pred.val += self.c1.val
            if succ: succ.val += self.c2.val

            self.c1 = None
            self.c2 = None
            self.val = 0

        else:
            self.c1.explode(level - 1)
            self.c2.explode(level - 1)

    def split(self):
        if self.val is not None:
            if self.val >= 10:
                self.c1 = Node(floor(self.val / 2), self)
                self.c2 = Node(ceil(self.val / 2), self)
                self.val = None
                return True
            return False
        else:
            didSplit = self.c1.split()

            if not didSplit:
                didSplit = self.c2.split()

            return didSplit
            
    def normalize(self):
        self.explode()

        while self.split():
            self.explode()

    def __add__(self, other):
        n = Node([self.to_list(), other.to_list()])
        n.normalize()

        return n

    def magnitude(self):
        if self.val is not None:
            return self.val
        return 3*self.c1.magnitude() + 2*self.c2.magnitude()

    def to_list(self):
        if self.val is not None:
            return self.val
        else:
            return [self.c1.to_list(), self.c2.to_list()]
    
with open("input.txt", "r") as f:
    nodes = [Node(eval(line)) for line in f]

    s = nodes[0]

    for node in nodes[1:]:
        s = s + node

    print(s.magnitude())

    print(max((n1+n2).magnitude() for n1,n2 in product(nodes, nodes)))
