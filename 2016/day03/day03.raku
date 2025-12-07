my @lines = do for "../inputs/day03-real.txt".IO.lines {
	my (Int() $a, Int() $b, Int() $c) := m:s/(\d+) (\d+) (\d+)/;
	($a, $b, $c)
};

sub match (@l) { {$^a + $^b > $^c}(|@l.sort) }

say @lines.grep(&match).elems;

say ([Z] @lines).flat.batch(3).grep(&match).elems;

