
lines(File, Lines) :-
	setup_call_cleanup(
		open(File, read, Stream),
		(
			read_string(Stream, _, String),
			split_string(String, "\n", "", Lines)
		),
		close(Stream)).

run_line(Dir, Dir, [""]).
run_line(_, ["/"], ["$", "cd", "/"]).
run_line([_|Parent], Parent, ["$", "cd", ".."]).
run_line(Dir, [NewDir|Dir], ["$", "cd", NewDir]) :- NewDir \= "..", NewDir \= "/".
run_line(Dir, Dir, ["$", "ls"]).
run_line(Dir, Dir, ["dir", _]).

run_line(Dir, Dir, [SizeStr, Name]) :-
	number_string(Size, SizeStr),
	assertz(file(Dir, Name, Size)).

run_lines(_, []).
run_lines(Dir, [L|Ls]) :-
	split_string(L, " ", "", Split),
	run_line(Dir, NewDir, Split),
	run_lines(NewDir, Ls).

run_input(File) :-
	abolish(file/3),
	abolish(folder/1),
	lines(File, Lines),
	run_lines(["/"], Lines),
	findall(Dir, file(Dir, _, _), Dirs),
	list_to_set(Dirs, DirSet),
	forall(member(D, DirSet), assertz(folder(D))).

%% folder_size(Dir, TotalSize) :-
%% 	findall(Dir, file(Dir, _, _), Paths),
%% 	list_to_set(Paths, Paths2),
%% 	member(Dir, Paths2),
%% 	findall(Size, (member(SubPath, Paths2), file(SubPath, _, Size)), Sizes),
%% 	foldl(plus, Sizes, 0, TotalSize).

	
folder_size(Dir, TotalSize) :-
	folder(Dir),
	findall(Size, (file(Path, _, Size), append(_, Dir, Path)), List),
	foldl(plus, List, 0, TotalSize).

small_folder_size(TotalSize) :-
	findall(Size, (folder_size(_, Size), Size =< 100000), Sizes),
	foldl(plus, Sizes, 0, TotalSize).

