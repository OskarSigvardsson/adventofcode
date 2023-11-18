#include <stdlib.h>
#include <stdio.h>


struct node {
	char c;
	struct node *prev;
	struct node *next;
};

void print(struct node *node) {
	node = node->next;
	while (node->c != 0) {
		printf("%c", node->c);
		node = node->next;
	}
	printf("\n");
}

struct node *copy_chain(struct node *copynode) {
	struct node *head = malloc(sizeof(struct node*));

	head->c = 0;
	head->next = head;
	head->prev = head;

	copynode = copynode->next;
	struct node *curr = head;
	
	while (copynode->c != 0) {
		struct node *new = malloc(sizeof(struct node*));

		new->c = copynode->c;
		new->prev = curr;
		curr->next = new;
		new->next = head;
		head->prev = new;

		curr = new;
		copynode = copynode->next;
	}

	return head;
}


void react(struct node *head) {
	struct node *curr = head->next;
	
	while (curr->c != 0) {
		//print(head);
		if (curr->next->c == 0) break;

		if (abs(curr->c - curr->next->c) == 32) {
			curr->prev->next = curr->next->next;
			curr->next->next->prev = curr->prev;
			curr = curr->prev;

			if (curr == head) {
				curr = head->next;
			}
		} else {
			curr = curr->next;
		}
	}
}

int main() {
	FILE *file = fopen("test.txt", "r");
	struct node *head = malloc(sizeof(struct node));
	struct node *curr = head;
	
	head->c = 0;
	head->next = head;
	head->prev = head;

	int c;
	while ((c = fgetc(file)) != '\n') {
		struct node *new = malloc(sizeof(struct node));

		new->c = c;
		new->prev = curr;
		curr->next = new;
		new->next = head;
		head->prev = new;

		curr = new;
	}

	struct node *copy = copy_chain(head);

	print(copy);
	print(head);
	return 0;

	react(head);

	int count = 0;
	curr = head->next;
	
	while (curr->c != 0) {
		count++;
		curr = curr->next;
	}

	printf("%d\n", count);
}

