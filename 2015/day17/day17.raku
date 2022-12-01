my @input = "input.txt".IO.lines>>.Int;

sub solve($index, $amount, @config = []) {
	when $amount < 0 { [] }
	when $index == @input.elems {
		if $amount == 0 {
			[@config,]
		} else {
			[]
		}
	}

	my $container = @input[$index];

	[|solve($index + 1, $amount, @config),
	 |solve($index + 1, $amount - $container, [|@config, $container])]
}

my @solves = solve(0, 150);
my $min = @solves>>.elems.min;

say @solves.elems;

say @solves.grep(*.elems == $min).elems;

