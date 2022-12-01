use JSON::Tiny;

my $input = "input.txt".IO.slurp.trim;

($input ~~ m:g/'-'? \d+/)>>.Num.sum.say;

multi sub calc-sum(Str $json) { 0 }
multi sub calc-sum(Num $json) { $json }
multi sub calc-sum(Int $json) { $json }

multi sub calc-sum(@json) { @json.map({calc-sum($_)}).sum }

multi sub calc-sum(%json) {
	when "red" ~~ %json.values.any { 0 }

	%json.values.map({calc-sum($_)}).sum
}

say calc-sum(from-json($input));
					   
