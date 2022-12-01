my @input = "input.txt".IO.slurp.trim.comb;
my %dirs = '>' => (1, 0), '^' => (0, 1), '<' => (-1, 0), 'v' => (0, -1);

sub part1 {
	my %houses = (0,0) => 1;
	my $pos = (0,0);

	for @input -> $d {
		$pos = $pos <<+>> %dirs{$d};
		%houses{$pos}++;
	}

	return %houses.keys.elems;
}

sub part2 {
	my %santa = (0,0) => 1;
	my %robot = (0,0) => 1;
	my $s = (0,0);
	my $r = (0,0);

	for @input -> $d1, $d2 {
		$s = $s <<+>> %dirs{$d1};
		$r = $r <<+>> %dirs{$d2};
		%santa{$s}++;
		%robot{$r}++;
	}

	return %(|%santa, |%robot).keys.elems;
}

say part1;
say part2;
