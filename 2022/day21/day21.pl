:- use_module(library(clpfd)).

lines(File, Lines) :-
	open(File, read, Stream),
	read_string(Stream, _, String),
	split_string(String, "\n", "", Lines),
	close(Stream).

parse([]) :- !.
parse([""|Ls]) :- !, parse(Ls).
parse([L|Ls]) :- 
	split_string(L, ": ", "", S),
	parse_(S), !,
	parse(Ls).

parse_(["root", "", ML, _, MR]) :-
	assert(
		(monkey("root", H, 1) :-
			 monkey(ML, H, VL),
			 monkey(MR, H, VR),
			 VL #= VR)).

parse_([M, "", ML, Op, MR]) :-
	assert(
		(monkey(M, H, V) :-
			 monkey(ML, H, VL),
			 monkey(MR, H, VR),
			 eval(VL, Op, VR, V))).


parse_(["humn", "", _]) :- 
	assert(monkey("humn", H, H)).

parse_([M, "", V]) :- 
	number_string(N, V),
	assert(monkey(M, _, N)).

eval(T1, "+", T2, R) :- R #= T1 + T2.
eval(T1, "-", T2, R) :- R #= T1 - T2.
eval(T1, "*", T2, R) :- R #= T1 * T2.
eval(T1, "/", T2, R) :- R #= T1 // T2.

load_input(File) :-
	untable(monkey/3),
	abolish(monkey/3),
	lines(File, Lines),
	parse(Lines).
