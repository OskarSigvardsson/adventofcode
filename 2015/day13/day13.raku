my @input = "input.txt".IO.lines;

my %happy1;
my $people1 = SetHash.new;

my rule format {
	(\w+) "would" ("gain"|"lose") (\d+)
	"happiness units by sitting next to"
	(\w+)
}

for @input {
	my ($a, $b, $c, $d) = |($_ ~~ &format)>>.Str;
	%happy1{$a => $d} = ($b ~~ "gain" ?? 1 !! -1) * $c.Int;
	$people1.set($a);
}

sub happiness(@order, %happy) {
	my $s = @order.elems;
	
	@order.kv.map({
		my $before = @order[($^a - 1) % $s];
		my $after  = @order[($^a + 1) % $s];
		%happy{$^b => $before} + %happy{$^b => $after}
	}).sum
}

say %happy1;

my %happy2 = %happy1.clone;
my $people2 = $people1.clone;

for $people1.keys {
	%happy2{"me" => $_} = 0;
	%happy2{$_ => "me"} = 0;
}

$people2.set("me");

say $people1.keys.permutations.map({happiness($_, %happy1)}).max;
say $people2.keys.permutations.map({happiness($_, %happy2)}).max;

