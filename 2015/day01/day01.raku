my @input = "input.txt".IO.slurp.trim.comb;

#part 1
my %count;
%count{$_}++ for @input;

say %count{"("} - %count{")"};

#part 2

my $floor = 0;
my %code = "(" => 1, ")" => -1;


for @input.map({ %code{$_} }).kv -> $i, $c {
	$floor += $c;
	if $floor < 0 {
		say $i + 1;
		last;
	}
}

