#include <stdbool.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>

struct segment {
    bool used;
    int16_t index;
    int32_t size;
    struct segment *next;
    struct segment *prev;
};

0123456789
..........
0123454589

static struct segment segment_pool[1000000];

int main() {
    struct segment *next_segment = segment_pool;

    FILE *file = fopen("../inputs/day09-real.txt", "r");

    struct segment head = {
        .used = false,
        .size = -1,
        .next = &head,
        .prev = &head,
    };

    int c;
    bool used = true;
    int16_t index = 0;

    while ((c = fgetc(file)) != EOF) {
        if (!isdigit(c)) continue;

        struct segment *link = next_segment++;
        link->used = used;
        link->index = index;
        link->size = (int32_t)(c - '0');
        link->prev = head.prev;
        link->next = &head;
        link->prev->next = link;
        link->next->prev = link;

        if (used) index++;
        used = !used;
    }

    struct segment *curr = head.prev;

    while (curr != &head) {
        if (!curr->used) {
            curr = curr->prev;
            continue;
        }
        
        for (struct segment *link = head.next->next; link != curr; link = link->next) {

            if (link->used || link->size < curr->size) {
                continue;
            }

            if (link->size != curr->size) {
                struct segment *new = next_segment++;
                new->used = false;
                new->index = -1;
                new->size = link->size - curr->size;
                new->next = link->next;
                new->prev = link;
                new->next->prev = new;
                new->prev->next = new;
            }

            link->used = true;
            link->index = curr->index;
            link->size = curr->size;

            curr->used = false;
            break;
        }
        
        curr = curr->prev;
    }

    int64_t checksum = 0;

    int i = 0;
    for (struct segment *link = head.next; link != &head; link = link->next) {
        if (!link->used) {
            i+=link->size;
        } else {
            for (int j = 0; j < link->size; j++) {
                checksum += link->index * i++;
            }
        }
    }

    printf("Checksum %lld\n", checksum);
}