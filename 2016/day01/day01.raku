my @insts = "../inputs/day01-real.txt".IO.slurp.split(",").map: { m/("R"|"L") (\d+) / }; 

my %turn = "L" => 1i, "R" => -1i;

my $p = 0i;
my $d = 1i;

for @insts -> ($a, $b) {
	# say $_[0].Str;
	# say $_[1].Int;
	$d *= %turn{$a.Str};
	$p += $d * $b.Int;
}

say abs($p.re) + abs($p.im);

$p = 0i;
$d = 1i;
my $visited = SetHash.new($p);

INST: for @insts -> ($a, $b) {
	$d *= %turn{$a.Str};

	for 1..$b.Int {
		$p += $d;
		last INST if $visited{$p};
		$visited.set($p);
	}
}

say abs($p.re) + abs($p.im);
