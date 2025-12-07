#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>

struct num_set {
	uint64_t coord;
	struct num_set *next;
};

void free_num_set(struct num_set *s) {
	while (s != NULL) {
		struct num_set *tmp = s;
		s = s->next;
		free(tmp);
	}
}

// s1 becomes the set union of s1 and s2
void join(struct num_set *s1, struct num_set *s2) {
	if (s1->coord > s2->coord) {
		uint64_t tmp = s1->coord;
		s1->coord = s2->coord;
		s2->coord = tmp;
	}
	
	struct num_set *head = s1;
	struct num_set *tail = s1;
	s1 = s1->next;
	
	while (s1 != NULL && s2 != NULL) {
		if (s1->coord == s2->coord) {
			struct num_set *tmp = s2;
			s2 = s2->next;
			free(tmp);
		} else if (s1->coord < s2->coord) {
			tail->next = s1;
			tail = s1;
			s1 = s1->next;
		} else {
			tail->next = s2;
			tail = s2;
			s2 = s2->next;
		}
	}
	
	if (s1 != NULL) tail->next = s1;
	if (s2 != NULL) tail->next = s2;
}

int main() {
}