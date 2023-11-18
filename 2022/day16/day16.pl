:- use_module(library(dcg/basics)).
:- set_prolog_flag(double_quotes, codes).

%valve(V) --> string(VStr), { length(VStr, 2), atom_codes(V, VStr) }.

parse_valve(V) --> [C1, C2], { atom_codes(V, [C1, C2]) }.
parse_conns([C|Cs]) --> parse_valve(C), (", ", parse_conns(Cs) | { Cs = [] }).
parse(Valve, Rate, Conns) -->
	"Valve ", parse_valve(Valve),
	" has flow rate=", integer(Rate), "; ",
	"tunnel", ("s" | ""), " lead", ("s"|""), " to valve", ("s"|""), " ", parse_conns(Conns).

load_file(File) :-
	abolish(valve/3),
	abolish(valves/1),
	open(File, read, Stream),
	load_stream(Stream),
	findall(Valve, valve(Valve, _, _), Valves),
	sort(Valves, Sorted),
	assertz(valves(Sorted)),
	close(Stream).
	
load_stream(Stream) :- at_end_of_stream(Stream), !.
load_stream(Stream) :-
	read_line_to_codes(Stream, Line),
	atom_codes(LineAtom, Line),
	format("~s~n", LineAtom),
	phrase(parse(Valve, Rate, Conns), Line),
	format("~s ~d ~q~n", [Valve, Rate, Conns]),
	assertz(valve(Valve, Rate, Conns)),
	load_stream(Stream).
	

%% open_valve(Valve, [Valve-open|Vs], [Valve-open|Vs]) :- !.
%% open_valve(Valve, [Valve-closed|Vs], [Valve-open|Vs]) :-
%% 	valve(Valve, _, _), !.

open_valve(Valve, [Valve-_|Vs], [Valve-open|Vs]) :- !.
open_valve(Valve, [V-S|Vs], [V-S|Rest]) :-
	Valve \== V,
	open_valve(Valve, Vs, Rest).

search(Flow) :-
	findall(Valve-closed, valve(Valve, _, _), Valves),
	Valves = [VH-closed|_],
	search(1, Valves, VH, Flow).

flow(Valves, Flow) :- flow(Valves, Flow, 0).

flow([], Acc, Acc).
flow([Valve-open|Vs], TotalFlow, Acc) :-
	valve(Valve, Flow, _),
	NewAcc is Acc + Flow,
	flow(Vs, TotalFlow, NewAcc).

flow([_-closed|Vs], Flow, Acc) :-
	flow(Vs, Flow, Acc).
	
search(30, _, _, 0).
search(Turn, Valves, Pos, Flow) :-
	Turn < 30,
	NextTurn is Turn + 1,
	valve(Pos, ThisFlow, Conns),
	( ThisFlow > 0
	-> (open_valve(Pos, Valves, StayValves),
		search(NextTurn, StayValves, Pos, StayFutureFlow),
		flow(StayValves, StayNowFlow),
		StayFlow is StayNowFlow + StayFutureFlow)
	; StayFlow = 0),

	flow(Valves, MoveNowFlow),
	maplist(search(NextTurn, Valves), Conns, MoveFutureFlows),
	maplist(plus(MoveNowFlow), MoveFutureFlows, MoveFlows),
	max_list([StayFlow | MoveFlows], Flow).
