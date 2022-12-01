my @input = "input.txt".IO.lines;
my %d;
my $cities = SetHash.new;

for @input {
	my ($c1, $c2, $d) = |m:s/(\w+) to (\w+) '=' (\d+)/;

	$c1 = $c1.Str;
	$c2 = $c2.Str;
	$d = $d.Num;
	
	%d{$c1 => $c2} = $d;
	%d{$c2 => $c1} = $d;

	$cities.set($c1);
	$cities.set($c2);
}

sub dist(@perm) {
	(for @perm Z @perm[1..*] -> ($a, $b) { %d{$a => $b} }).sum
}

say (for $cities.keys.permutations { dist(@_) }).min;
say (for $cities.keys.permutations { dist(@_) }).max;

