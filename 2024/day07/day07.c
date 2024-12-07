#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

struct num_list {
    int64_t n;
    struct num_list *next;
};

int64_t add(int64_t a, int64_t b) {
    return a + b;
}

int64_t mul(int64_t a, int64_t b) {
    return a * b;
}

int64_t cat(int64_t a, int64_t b) {
    int pow = 10;
    while (pow <= b) pow *= 10;
    return a * pow + b;
}

typedef int64_t (*op)(int64_t, int64_t);

bool solvable(int64_t ans, struct num_list *ns, op *ops) {
    if (ns->next == NULL) {
        return ns->n == ans;
    }

    int64_t a = ns->n;
    int64_t b = ns->next->n;

    op *curr = ops;
    while(*curr != NULL) {
        int64_t c = (*curr)(a, b);

        ns->next->n = c;
        bool ok = solvable(ans, ns->next, ops);
        ns->next->n = b;

        if (ok) return true;
        curr++;
    }
    return false;
}

int fpeek(FILE *f)
{
    int c;

    c = fgetc(f);
    ungetc(c, f);

    return c;
}

int main() {
    FILE *file = fopen("../inputs/day07-real.txt", "r");

    int64_t p1 = 0;
    int64_t p2 = 0;

    while (true) {
        int64_t ans; 
        int args = fscanf(file, "%lld:", &ans);

        if (args != 1) break;

        struct num_list *head = NULL;
        struct num_list *tail = NULL;

        while (fpeek(file) != '\n') {
            struct num_list *n = malloc(sizeof(struct num_list));
            int args = fscanf(file, " %lld", &(n->n));
            if (args != 1) break;

            if (head == NULL) {
                head = n;
                tail = n;
            } else {
                tail->next = n;
                tail = n;
            }
        }

        op p1_ops[] = { add, mul, NULL };
        op p2_ops[] = { add, mul, cat, NULL };

        if (solvable(ans, head, p1_ops)) { p1 += ans; }
        if (solvable(ans, head, p2_ops)) { p2 += ans; }
    }

    printf("Part 1: %lld\n", p1);
    printf("Part 2: %lld\n", p2);

    return 0;
}