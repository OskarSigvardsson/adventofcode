sub doubles(@list) {
	@list Z @list[1..*]
}

sub triples(@list) {
	@list Z @list[1..*] Z @list[2..*]
}

sub increasing(@list) {
	do for doubles(@list) -> ($a,$b) {
		$b == $a + 1
	}.all.Bool
}

sub has-increasing($pass) {
	increasing(triples($pass.comb.map(*.ord)).any).Bool;
}

sub has-not-iol($pass) {
	!($pass ~~ m/i|o|l/).Bool
}

sub has-doubles($pass) {
	($pass ~~ m:g/(.)$0/)>>.Str.SetHash.elems >= 2
}

sub admissible($pass) {
	has-increasing($pass) && has-not-iol($pass) && has-doubles($pass)
}

sub succ($pass) {
	my $a = 'a'.ord;
	my $count = 'z'.ord - 'a'.ord + 1;
	
	my @nums = $pass.comb>>.ord.map(* - $a).reverse;

	for @nums.kv -> $i,$n {
		@nums[$i] = ($n + 1) % $count;

		if @nums[$i] != 0 { last; }
	}

	@nums.reverse.map(* + $a)>>.chr.join
}

sub next($in) {
	my $pass = succ($in);
	
	while !admissible($pass) {
		$pass = succ($pass);
	}
	$pass
}

my $input = "hepxcrrq";
my $n1 = next($input);
say $n1;
my $n2 = next($n1);
say $n2;


