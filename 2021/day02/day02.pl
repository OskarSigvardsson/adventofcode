:- ['../utils.pl'].

actions(As) :-
	findall(
		Pair,
		( file_line("input.txt", L),
		  split_string(L, " ", "", [Act, V]),
		  number_string(N, V),
		  Pair = Act - N ),
		As).

%% part 1
update1("forward" - N, X1, Y, X2, Y) :- X2 is X1 + N.
update1("up"      - N, X, Y1, X, Y2) :- Y2 is Y1 - N.
update1("down"    - N, X, Y1, X, Y2) :- Y2 is Y1 + N.

part1([], X, Y, Res) :- Res is X * Y.
part1([A-N|Tail], X1, Y1, Res) :-
	update1(A-N, X1, Y1, X2, Y2),
	part1(Tail, X2, Y2, Res).
	
part1(Acts, Res) :- part1(Acts, 0, 0, Res).


% part 2
update2("forward" - N, A1, D1, F1, A1, D2, F2) :- F2 is F1 + N, D2 is D1 + A1 * N.
update2("up"      - N, A1, D1, F1, A2, D1, F1) :- A2 is A1 - N.
update2("down"    - N, A1, D1, F1, A2, D1, F1) :- A2 is A1 + N.

part2([], _, D, F, Res) :- Res is D * F.
part2([A-N|Tail], A1, D1, F1, Res) :-
	update2(A-N, A1, D1, F1, A2, D2, F2),
	part2(Tail, A2, D2, F2, Res).
	
part2(Acts, Res) :- part2(Acts, 0, 0, 0, Res).

:- actions(As),
   part1(As, P1),
   part2(As, P2),
   format("Part 1: ~d~n", P1),
   format("Part 2: ~d~n", P2).
	
