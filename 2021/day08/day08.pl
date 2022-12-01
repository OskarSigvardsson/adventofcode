:- ['../utils.pl'].

%%   0:      1:      2:      3:      4:
%%  aaaa    ....    aaaa    aaaa    ....
%% b    c  .    c  .    c  .    c  b    c
%% b    c  .    c  .    c  .    c  b    c
%%  ....    ....    dddd    dddd    dddd
%% e    f  .    f  e    .  .    f  .    f
%% e    f  .    f  e    .  .    f  .    f
%%  gggg    ....    gggg    gggg    ....
%% 
%%   5:      6:      7:      8:      9:
%%  aaaa    aaaa    aaaa    aaaa    aaaa
%% b    .  b    .  .    c  b    c  b    c
%% b    .  b    .  .    c  b    c  b    c
%%  dddd    dddd    ....    dddd    dddd
%% .    f  e    f  .    f  e    f  .    f
%% .    f  e    f  .    f  e    f  .    f
%%  gggg    gggg    ....    gggg    gggg

% segment definitions
segment(0, [a, b, c, e, f, g]).
segment(1, [c, f]).
segment(2, [a, c, d, e, g]).
segment(3, [a, c, d, f, g]).
segment(4, [b, c, d, f]).
segment(5, [a, b, d, f, g]).
segment(6, [a, b, d, e, f, g]).
segment(7, [a, c, f]).
segment(8, [a, b, c, d, e, f, g]).
segment(9, [a, b, c, d, f, g]).

% this maps a group to a new group given a certain mapping
mapgroup([], [], _).
mapgroup([U|Us], [M|Ms], Map) :- member(U-M, Map), mapgroup(Us, Ms, Map).

% this is the core of the algorithm: given a set a of groups, it either checks
% or generates a valid mapping
solve([], _).
solve([Group|Groups], Map) :-
	mapgroup(Group, Mapped, Map),
	segment(_, L), permutation(Mapped, L),
	solve(Groups, Map).

% helper function to turn an output group into a number using a mapping
output_number([], _, Res, Res).
output_number([O|Os], Map, Acc1, Res) :-
	mapgroup(O, P, Map),
	segment(N, L),
	permutation(P, L),
	Acc2 is Acc1 * 10 + N,
	output_number(Os, Map, Acc2, Res).
	
% Loop through all the inputs, genereate the output_numbers, sum it all up
part2([], [], Res, Res).
part2([In|Ins], [Out|Outs], Acc1, Res) :-
	Map = [a-_,b-_,c-_,d-_,e-_,f-_,g-_],
	solve(In, Map),
	output_number(Out, Map, 0, Ns),
	Acc2 is Acc1 + Ns,
	part2(Ins, Outs, Acc2, Res).

% the rest of this is just parsing
inputs(Inputs, Outputs) :-
	findall(
		Is - Os,
		( file_line("input.txt", L),
		  split_string(L, "|", " ", [Is, Os])),
		Pairs),
	findall(R, member(R-_, Pairs), InStr),
	findall(L, member(_-L, Pairs), OutStr),
	maplist(to_atoms, InStr, Inputs),
	maplist(to_atoms, OutStr, Outputs).

to_atoms(Str, Atoms) :-
	split_string(Str, " ", "", L),
	maplist(string_atoms, L, Atoms).
	
string_atoms(Str, Atoms) :-
	string_codes(Str, Codes),
	findall(Atom, (member(C, Codes), atom_codes(Atom, [C])), Atoms).


:- inputs(Ins, Outs),
   part2(Ins, Outs, 0, Res),
   format("~d~n", Res),
   halt.
