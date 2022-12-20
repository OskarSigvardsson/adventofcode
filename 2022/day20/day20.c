#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>

struct link {
	int64_t val;
	struct link *prev;
	struct link *next;
};

struct orig {
	struct link *item;
	struct orig *next;
};

void print(struct link *list) {
	struct link *curr = list;
	do {
		printf("%lld ", curr->val);
		curr = curr->next;
	} while (curr != list);
	printf("\n");
}

int64_t sgn(int64_t v) {
	return v == 0 ? 0 : v < 0 ? -1 : 1;
}

void mix(struct orig *ol, int64_t length) {
	while (ol) {
		struct link *li = ol->item;

		int64_t c = llabs(li->val) % (length - 1);
		
		for (int64_t i = 0; i < c; i++) {
			struct link *l0, *l1, *l2, *l3;

			if (li->val < 0) {
				l0 = li->prev->prev;
				l1 = li->prev;
				l2 = li;
				l3 = li->next;
			} else {
				l0 = li->prev;
				l1 = li;
				l2 = li->next;
				l3 = li->next->next;
			}

			l0->next = l2;
			l3->prev = l1;
			l1->next = l3;
			l2->prev = l0;
			l1->prev = l2;
			l2->next = l1;
		}

		ol = ol->next;
	}
}

int main() {
	FILE *f = fopen("input.txt", "r");
	char buf[64];
	int64_t length = 0;
	
	struct link scaffold;

	scaffold.val = 0;
	scaffold.prev = &scaffold;
	scaffold.next = &scaffold;

	struct link *ll = &scaffold;

	struct orig *ohead = NULL;
	struct orig **optr = &ohead;
	
	while (fgets(buf, 64, f)) {
		length++;
		
		struct link *le = malloc(sizeof(struct link));
		struct orig *oe = malloc(sizeof(struct orig));
		
		oe->item = le;
		oe->next = NULL;

		*optr = oe;
		optr = &(oe->next);
		
		le->val = atoll(buf) * 811589153ll;
		le->prev = ll;
		le->next = ll->next;

		ll->next->prev = le;
		ll->next = le;

		ll = le;
	}

	scaffold.prev->next = scaffold.next;
	scaffold.next->prev = scaffold.prev;
	ll = scaffold.next;

	mix(ohead, length);
	mix(ohead, length);
	mix(ohead, length);
	mix(ohead, length);
	mix(ohead, length);
	mix(ohead, length);
	mix(ohead, length);
	mix(ohead, length);
	mix(ohead, length);
	mix(ohead, length);

	//print(ll);

	while (ll->val != 0) ll = ll->next;

	int64_t sum = 0;
	
	for (int64_t i = 1; i <= 3000; i++) {
		ll = ll->next;

		if (i == 1000 || i == 2000 || i == 3000) {
			sum += ll->val;
		}
	}

	printf("%lld\n", sum);
}
