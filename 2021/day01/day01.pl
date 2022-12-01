:- ['../utils.pl'].

soundings(Ns) :- findall(N, (file_line("input.txt", L), number_string(N, L)), Ns).

part1([_], Acc, Acc).
part1([A,B|Tail], Acc, Res) :-
	(A < B
	->  Acc2 is Acc + 1
	;   Acc2 is Acc),
	part1([B|Tail], Acc2, Res).

part2([_,_,_], Acc, Acc).
part2([A,B,C,D|Tail], Acc, Res) :-
	W1 is A + B + C,
	W2 is B + C + D,
	(W1 < W2
	->  Acc2 is Acc + 1
	;   Acc2 is Acc),
	part2([B,C,D|Tail], Acc2, Res).

:- soundings(Ns),
   part1(Ns, 0, P1),
   part2(Ns, 0, P2),
   format("Part 1: ~d~n", P1),
   format("Part 2: ~d~n", P2).
