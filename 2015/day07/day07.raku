my @input = "input.txt".IO.lines;

grammar Op {
	token const { \d+ }
	token ident { \w+ }
	token arg1 { <const> | <ident> }
	token arg2 { <const> | <ident> }
	token target { <ident> }
	
	proto token op {*}
	token op:sym<AND>    { <sym> }
	token op:sym<OR>     { <sym> }
	token op:sym<NOT>    { <sym> }
	token op:sym<LSHIFT> { <sym> }
	token op:sym<RSHIFT> { <sym> }

	rule assign { <arg1> }
	rule single { <op> <arg1> }
	rule double { <arg1> <op> <arg2> }
	
	rule TOP { [ <arg1> | <op> <arg2> | <arg1> <op> <arg2> ] '->' <target> }
}

my %rules;
my %values;

sub eval($target) {

	when ($target ~~ /\d+/) { $target.Int }
	when $target ~~ %values { %values{$target} }

	my $command = %rules{$target};
	
	my uint16 $val = do given $command<op> {
		when Nil      { eval($command<arg1>)                         }
		when "AND"    { eval($command<arg1>) +& eval($command<arg2>) }
		when "OR"     { eval($command<arg1>) +| eval($command<arg2>) }
		when "NOT"    {                      +^ eval($command<arg2>) }
		when "LSHIFT" { eval($command<arg1>) +< eval($command<arg2>) }
		when "RSHIFT" { eval($command<arg1>) +> eval($command<arg2>) }
	}

	%values{$target} = $val;

	$val
}

#@input = ("NOT 123 -> x");

for @input -> $line {
	my $parse = Op.parse($line);
	%rules{$parse<target>} = $parse;
}

say eval("a");

%values = b => %values<a>;

say eval("a");
