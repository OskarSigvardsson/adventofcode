:- ['../utils.pl'].

hex("0", [0, 0, 0, 0]).
hex("1", [0, 0, 0, 1]).
hex("2", [0, 0, 1, 0]).
hex("3", [0, 0, 1, 1]).
hex("4", [0, 1, 0, 0]).
hex("5", [0, 1, 0, 1]).
hex("6", [0, 1, 1, 0]).
hex("7", [0, 1, 1, 1]).
hex("8", [1, 0, 0, 0]).
hex("9", [1, 0, 0, 1]).
hex("A", [1, 0, 1, 0]).
hex("B", [1, 0, 1, 1]).
hex("C", [1, 1, 0, 0]).
hex("D", [1, 1, 0, 1]).
hex("E", [1, 1, 1, 0]).
hex("F", [1, 1, 1, 1]).

bin_int([], Acc, Acc).
bin_int([H|T], Acc1, Res) :-
	Acc2 is Acc1 * 2 + H,
	bin_int(T, Acc2, Res).

bin_int(Bs, I) :- bin_int(Bs, 0, I).
bin_int_r(Bs, I) :- reverse(Bs, Brs), bin_int(Brs, 0, I).

bits(Bs) :-
	file_line("input.txt", L), !,
	findall(
		Hs,
		( sub_string(L, _, 1, _, C), hex(C, Hs) ),
		Bns),
	flatten(Bns, Bs).

parse(Str, Ps) :-
	findall(Hs, (sub_string(Str, _, 1, _, C), hex(C, Hs)), Nested),
	flatten(Nested, Bits),
	packets(Bits, [Ps]).

int_chunks([0,B1,B2,B3,B4|T], [B1,B2,B3,B4], T).
int_chunks([1,B1,B2,B3,B4|T], L, Rest) :-
	int_chunks(T, L1, Rest),
	append([B1,B2,B3,B4], L1, L).

literal(T, I, Rest) :- int_chunks(T, B, Rest), bin_int(B, I).

packet([V1,V2,V3,1,0,0|T], i(V, I), Rest) :-
	bin_int([V1,V2,V3], V),
	literal(T, I, Rest).

packet([V1,V2,V3,T1,T2,T3,0|T], o(V, Type, Ps), Rest) :-
	[T1,T2,T3] \= [1,0,0],
	bin_int([T1,T2,T3], Type),
	bin_int([V1,V2,V3], V),
	length(LengthBin, 15),
	append(LengthBin, Rest1, T),
	bin_int(LengthBin, Length),
	length(Contents, Length),
	append(Contents, Rest, Rest1),
	packets(Contents, [], Psr),
	reverse(Ps, Psr).

packet([V1,V2,V3,T1,T2,T3,1|T], o(V, Type, Ps), Rest) :-
	[T1,T2,T3] \= [1,0,0],
	bin_int([T1,T2,T3], Type),
	bin_int([V1,V2,V3], V),
	length(CountBin, 11),
	append(CountBin, Rest1, T),
	bin_int(CountBin, Count),
	npackets(Count, Rest1, Rest, [], Psr),
	reverse(Ps, Psr).
	
zeroes([]).
zeroes([0|T]) :- zeroes(T).

npackets(0, T, T, Res, Res).
npackets(N, Bits, Rest, Acc, Res) :-
	N > 0, N1 is N - 1,
	packet(Bits, P, Tail),
	npackets(N1, Tail, Rest, [P|Acc], Res).

packets(L, Ps) :- packets(L, [], Ps).
packets(Z, Acc, Acc) :- zeroes(Z).
packets(L, Acc, Res) :-
	packet(L, P, T),
	packets(T, [P|Acc], Res).



version_sum(i(V, _), V).
version_sum(o(V, _, Sub), V2) :-
	maplist(version_sum, Sub, Ns),
	foldl(plus, [V|Ns], 0, V2).

mul(A,B,C) :- C is A * B.
min(A,B,C) :- C is min(A, B).
max(A,B,C) :- C is max(A, B).

eval(i(_, I), I).

eval(o(_, 0, Ps), N) :- maplist(eval, Ps, Ns), foldl(plus, Ns, 0, N).
eval(o(_, 1, Ps), N) :- maplist(eval, Ps, Ns), foldl(mul, Ns, 1, N).
eval(o(_, 2, Ps), N) :- maplist(eval, Ps, [H|T]), foldl(min, T, H, N).
eval(o(_, 3, Ps), N) :- maplist(eval, Ps, [H|T]), foldl(max, T, H, N).

eval(o(_, 5, [A,B]), N) :- eval(A, N1), eval(B, N2), (N1  >  N2 -> N = 1 ; N = 0).
eval(o(_, 6, [A,B]), N) :- eval(A, N1), eval(B, N2), (N1  <  N2 -> N = 1 ; N = 0).
eval(o(_, 7, [A,B]), N) :- eval(A, N1), eval(B, N2), (N1 =:= N2 -> N = 1 ; N = 0).
	


