
% points table
points(rock,    rock,    4).
points(rock,    paper,   8).
points(rock,    scissor, 3).
points(paper,   rock,    1).
points(paper,   paper,   5).
points(paper,   scissor, 9).
points(scissor, rock,    7).
points(scissor, paper,   2).
points(scissor, scissor, 6).

% what beats what
beats(rock, scissor).
beats(scissor, paper).
beats(paper, rock).

% atom to weapon map
p1('A', rock). p1('B', paper). p1('C', scissor).
p2('X', rock). p2('Y', paper). p2('Z', scissor).

% picking your move based on strategy (part 2)
pick(Opponent, You, 'X') :- beats(Opponent, You).
pick(Opponent, You, 'Y') :- Opponent = You.
pick(Opponent, You, 'Z') :- beats(You, Opponent).

part1([], 0).
part1([[P1,P2]|Ls], Score) :-
	p1(P1, W1),
	p2(P2, W2),
	points(W1, W2, P),
	part1(Ls, RecScore),
	Score is RecScore + P.
	
part2([], 0).
part2([[P1, Strat] | Ls], Score) :-
	p1(P1, Opponent),
	pick(Opponent, You, Strat),
	points(Opponent, You, Points),
	part2(Ls, RecScore),
	Score is RecScore + Points.


% I/O stuff. the lines predicate unifies with the lines with the two columns as
% atoms
lines(File, Lines) :- findall(Line, file_line(File, Line), Lines).

file_line(File, [P1, P2]) :-
    setup_call_cleanup(open(File, read, In),
        (stream_line(In, [C1, _, C2]),
		atom_codes(P1, [C1]),
		atom_codes(P2, [C2])),
        close(In)).

stream_line(In, Line) :-
    repeat,
    (   read_line_to_codes(In, Line0),
        Line0 \== end_of_file
    ->  Line0 = Line
    ;   !,
        fail
    ).
