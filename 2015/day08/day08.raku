my @input = "input.txt".IO.lines;

sub unescape($str) {
	my $q = '"';
	my $b = '\\';
	my $new = $str;
	
	$new ~~ s:g/^'"'//;
	$new ~~ s:g/'"'$//;
	$new ~~ s:g/'\\\\'/$b/;
	$new ~~ s:g/'\\"'/$q/;
	$new ~~ s:g/'\\x'(<[0..9 a..f]> ** 2)/X/;

	$new
}

sub escape($str) {
	my $q = '"';
	my $b = "\\";
	
	my $new = $str;

	$new ~~ s:g/$b/$b$b/;
	$new ~~ s:g/$q/$b$q/;
	
	"\"$new\""
}


my @unescaped = @input.map({unescape($_)});
my @escaped = @input.map({escape($_)});

say @input.map(*.chars).sum - @unescaped.map(*.chars).sum;
say @escaped.map(*.chars).sum - @input.map(*.chars).sum;

for @input Z @escaped -> ($a, $b) {
	say $a;
	say $b;
}


