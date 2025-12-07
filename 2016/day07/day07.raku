my @lines = "../inputs/day07-test.txt".IO.lines; 

say "start";
sub slices(@elems, $n) {
	lazy gather {
		for [^(@elems.elems - $n + 1)] -> $i {
			take @elems[$i..($i+$n-1)];
		}
	}
}

sub has-abba(Str() $str --> Bool) {
	my @chrs = $str.comb;
	
	my @abbas = do for slices(@chrs, 4) -> ($a, $b, $c, $d) {
		$a eq $d and $b eq $c and not ($a eq $b)
	}

	@abbas.any.Bool
}

sub list-abas(Str() $str) {
	my @chrs = $str.comb;
	
	gather {
		for slices($str.comb, 3) -> ($a, $b, $c) {
			take ($a, $b, $c) if $a eq $c and not ($a eq $b)
		}
	}
}

sub babify(@str) {
	(@str[1], @str[0], @str[1])
}

my @part1 = do for @lines {
	my $in = 0;
	my $out = 0;
	for m:g/(\w+) (\[ \w+ \])?/ -> ($a, $b? = ""){
		$in++ if has-abba($a);
		$out++ if has-abba($b);
	}

	$in > 0 and $out == 0
}

say @part1.Bag{True};

my @part2 = do for @lines {
	my @abas;
	my @babs;
	
	for m:g/(\w+) (\[ \w+ \])?/ -> ($a, $b? = ""){
		@abas.append: list-abas($a);
		@babs.append: list-abas($b);
	}

	say @abas;
	say @babs;

	my $ret = False;
	for @abas -> $aba {
		return True if babify($aba) (elem) @babs;
	}
	return False;
}

say @part2.Bag{True};
