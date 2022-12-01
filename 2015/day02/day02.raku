my @lines = "input.txt".IO.lines;

my @sizes = @lines.map({ ($_ ~~ m/(\d+) 'x' (\d+) 'x' (\d+)/).list>>.Int });

sub paper($w, $h, $d) {
	my $s1 = $w * $h;
	my $s2 = $w * $d;
	my $s3 = $h * $d;
	
	return 2 * ($s1 + $s2 + $s3) + min($s1, $s2, $s3);
}

sub ribbon($w, $h, $d) {
	my $s1 = 2 * ($w + $h);
	my $s2 = 2 * ($w + $d);
	my $s3 = 2 * ($h + $d);

	return min($s1, $s2, $s3) + $w * $h * $d;
}

say @sizes.map({paper(|$_)}).sum;
say @sizes.map({ribbon(|$_)}).sum;

