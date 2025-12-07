my @lines = do for "../inputs/day04-real.txt".IO.lines {
	my (Str() $str, Int() $num, $check) := m/(.*) "-" (\d+) "[" (.*) "]"/;
	$str, $num, $check
}

my @act = @lines.grep: -> ($str, $num, $check) {
	# say $check;
	# say $str;
	my $code = $str.comb.grep(none '-').Bag.antipairs.sort(
	-> $a,$b {
		if $a.key == $b.key {
			$a.value cmp $b.value
		} else {
			$b.key cmp $a.key
		}
	}).map(-> $a { $a.value })[^5].join("");

	$code eq $check
};

say @act.map(*[1]).sum;

my @alphabet = "abcdefghijklmnopqrstuvwxyz";


for @lines -> ($str, $num, $check) {
	sub crack($c) {
		if $c ~~ "-" {
			$c
		} else {
			(($c.ord - 'a'.ord + $num) % 26 + 'a'.ord).chr
		}
	}

	say $str.comb.map(&crack).join(''), " ", $num;
	# say $str.comb.map((*.ord - 'a'.ord + 1))
	# 	.map(* % ('z'.ord - 'a'.ord))
	# 	.map(* + 'a'.ord)
	# 	.map(*.chr)
	# 	.join('');
}
