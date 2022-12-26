:- use_module(library(clpfd)).

snafu_digit('=', -2).
snafu_digit('-', -1).
snafu_digit('0', 0).
snafu_digit('1', 1).
snafu_digit('2', 2).

number_snafu(0, []) :- !.
number_snafu(D, [S|Ss]) :-
	D1 #= (D - 3) mod 5 - 2,
	D2 #= (D - D1) // 5,
	snafu_digit(S, D1),
	number_snafu(D2, Ss).
   
lines(File, Lines) :-
	open(File, read, Stream),
	read_string(Stream, _, String),
	split_string(String, "\n", "", Lines),
	close(Stream).

snafu_sum(Lines, SnafuStr) :-
	maplist(string_chars, Lines, CharLines),
	maplist(reverse, CharLines, RevLines),
	maplist(number_snafu, Nums, RevLines),
	foldl(plus, Nums, 0, Sum),
	number_snafu(Sum, Snafu),
	reverse(Snafu, SnafuRev),
	string_chars(SnafuStr, SnafuRev).
	
