my @input = "input.txt".IO.lines;
my %lights;

my regex on { :s turn on (\d+)\,(\d+) through (\d+)\,(\d+) };
my regex off { :s turn off (\d+)\,(\d+) through (\d+)\,(\d+) };
my regex toggle { :s toggle (\d+)\,(\d+) through (\d+)\,(\d+) };


sub part1 {
	for (0..999) X (0..999) -> $c {
		%lights{$c} = False;
	}

	for @input.kv -> $n, $line {
		say "$n/", @input.elems;

		given $line {
			when &on {
				%lights{$_} = True for [($0..$2) X ($1..$3)].race;
			}
			when &off {
				%lights{$_} = False for [($0..$2) X ($1..$3)].race;
			}
			when &toggle {
				%lights{$_} = !%lights{$_} for [($0..$2) X ($1..$3)].race;
			}
		};
	}

	return %lights.values.grep(* == True).elems;
}

sub part2 {
	for (0..999) X (0..999) -> $c {
		%lights{$c} = 0;
	}

	for @input.kv -> $n, $line {
		given $line {
			when &on {
				%lights{$_}++ for [($0..$2) X ($1..$3)].race;
			}
			when &off {
				%lights{$_} = max(%lights{$_} - 1, 0) for [($0..$2) X ($1..$3)].race;
			}
			when &toggle {
				%lights{$_} += 2 for [($0..$2) X ($1..$3)].race;
			}
		};
	}

	return %lights.values.sum;
}

say "Part 1: ", part1;
say "Part 2: ", part2;
