:- use_module(library(md5)).

hash(Prefix, Number, Hash) :-
	number_string(Number, Suffix),
	string_concat(Prefix, Suffix, String),
	md5_hash(String, Hash, []).

zeroes(0, "").
zeroes(N, String) :-
	N > 0,
	N2 is N - 1,
	zeroes(N2, Rest),
	string_concat("0", Rest, String).

find_num(Prefix, Zeroes, Number) :-
	zeroes(Zeroes, Target),
	find_num_(Prefix, Target, Number, 0).

find_num_(Prefix, Target, Current, Current) :-
	hash(Prefix, Current, Hash),
	string_concat(Target, _, Hash).

find_num_(Prefix, Target, Number, Current) :-
	Next is Current + 1,
	find_num_(Prefix, Target, Number, Next).

