my @input = "input.txt".IO.lines;

say "abcdef".comb.grep(* ~~ any "aeiou".comb).elems;
say "abcdef" ~~ /(qi|de)/;

sub nice1 ($s) {
	my $vowels = $s.comb.grep(* ~~ any "aeiou".comb).elems >= 3;
	my $repeat = $s ~~ /(.)$0/;
	my $banned = $s ~~ /(ab|cd|pq|xy)/;

	return $vowels && $repeat && !$banned;
}

sub nice2 ($s) {
	my $repeat = $s ~~ /(..) .* $0/;
	my $mixed = $s ~~ /(.) . $0/;

	return $repeat && $mixed;
}

say @input.grep({ nice1($_) }).elems;
say @input.grep({ nice2($_) }).elems;
