sub md5($str) {
	my $proc = run "md5sum", :out :in;

	$proc.in.spurt($str);
	$proc.in.close;
	$proc.out.slurp.split(" ")[0]
}

#say md5("abc3231929");

sub pass($head) {
	my @hashes = [^Inf].map($head ~ *).hyper(degree => 32).map(&md5).grep(*.starts-with("00000"))[^8];

	@hashes.map(*.comb[5]).join('')
}

say pass("abc");
