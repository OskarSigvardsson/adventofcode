my $target = 2504;
my @input = "input.txt".IO.lines;

my $format = rx:s/
	(\w+) "can fly" (\d+) "km/s for" (\d+)
	"seconds, but then must rest for" (\d+) "seconds."
/;

my %reindeer = @input.map({ if $_ ~~ $format { $0 => ($1.Num, $2.Num, $3.Num) } });

say %reindeer;

sub run-reindeer($speed, $duration, $rest) {
	lazy gather {
		my $pos = 0;

		take $pos;
		loop {
			take $pos += $speed for 1..$duration;
			take $pos for 1..$rest;
		}
	}
}


for %reindeer.kv -> $r, @s {
	say "$r:\t", run-reindeer(|@s)[$target];
}

my %runs = %reindeer.kv.map(-> $k, @v { $k => run-reindeer(|@v) });
my %points = %reindeer.keys.map(* => 0);

for 1..$target -> $i {
	my $max = %runs.values.map(*[$i]).max;
	

	for %runs.keys.grep({%runs{$_}[$i] == $max}) {
		%points{$_}++;
	}
}

say %points;
say %points.values.max;


# my @comet = reindeer(14, 10, 127);
# my @dancer = reindeer(16, 11, 162);
# my $dist = 2502;

# say @comet[$dist];
# say @dancer[$dist];

