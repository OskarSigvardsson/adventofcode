#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// struct num_list {
//     int64_t n;
//     struct num_list *next;
// };

// int64_t add(int64_t a, int64_t b) {
//     return a + b;
// }
// 
// int64_t mul(int64_t a, int64_t b) {
//     return a * b;
// }

int64_t cat(int64_t a, int64_t b) {
    int pow = 10;
    while (pow <= b) pow *= 10;
    return a * pow + b;
}

//typedef int64_t (*op)(int64_t, int64_t);

bool part1(int64_t ans, int64_t *ns) {
    if (ns[1] == -1) {
        return *ns == ans;
    }
    
    if (*ns > ans) return false;

    int64_t a = ns[0];
    int64_t b = ns[1];

    int64_t c;

    c = ns[0] + ns[1];
    if (part1(ans, ns+1)) return true;

    c = ns[0] * ns[1];
    if (part1(ans, ns+1)) return true;
    
    ns[1] = b;

    return false;
}

bool part2(int64_t ans, int64_t *ns) {
    if (ns[1] == -1) {
        return *ns == ans;
    }
    
    if (*ns > ans) return false;

    int64_t a = ns[0];
    int64_t b = ns[1];

    int64_t c;

    c = ns[0] + ns[1];
    if (part2(ans, ns+1)) return true;

    c = ns[0] * ns[1];
    if (part2(ans, ns+1)) return true;

    c = cat(ns[0],ns[1]);
    if (part2(ans, ns+1)) return true;
    
    ns[1] = b;

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

    int64_t ns[256];

    while (true) {
        int64_t ans; 
        int args = fscanf(file, "%lld:", &ans);

        if (args != 1) break;

        int i = 0;
        while (fpeek(file) != '\n') {
            // struct num_list *n = malloc(sizeof(struct num_list));
            int64_t n;
            int args = fscanf(file, " %lld", &n);
            if (args != 1) break;

            ns[i++] = n;
        }
        ns[i] = -1;

        // op p1_ops[] = { add, mul, NULL };
        // op p2_ops[] = { add, mul, cat, NULL };

        if (part1(ans, ns)) { p1 += ans; }
        if (part2(ans, ns)) { p2 += ans; }
    }

    printf("Part 1: %lld\n", p1);
    printf("Part 2: %lld\n", p2);

    return 0;
}