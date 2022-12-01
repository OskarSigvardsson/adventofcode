#my $input = "1113122113";



my $input = "1";

for 1..9 {
	$input ~~ s:g/ (\d) $0* /{$/.Str.chars ~ $0}/;
	say $input;
}

					 
