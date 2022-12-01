my $inputs = Channel.new;
my $outputs = Channel.new;

start {
	react {
		whenever $inputs {
			my $p = run 'md5sum', :in, :out;
			$p.in.print($_);
			$p.in.close();
			say $p.out.slurp;
		}
	}
}

$inputs.send("abcdef609043");
$inputs.close();
