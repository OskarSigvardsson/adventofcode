my @lines = "../inputs/day02-real.txt".IO.lines.list; 
my %dirs =
	U => (0,-1),
	D => (0,1),
	L => (-1,0),
	R => (1,0);

my @p = (1,1);
			
sub to-num($x,$y) { $y*3 + $x + 1 }

my @part1 = do for @lines -> $line {
	for $line.comb -> $chr {
		@p >>+=>> %dirs{$chr};
		@p = @p.map: { max(0,min(2,$_)) };
	}
	to-num(|@p)
};

say join "", @part1;

@p = (-2,0);

sub inside(@p) { @p.map(*.abs).sum < 3 }

my @map = ((1,),(2,3,4),(5,6,7,8,9),(10,11,12),(13,));
my @xo = (0,1,2,1,0);

sub to-num2($x,$y) {
	@map[$y+2][$x+@xo[$y+2]]
}

my @part2 = do for @lines -> $line {
	for $line.comb -> $chr {
		my @np = @p >>+>> %dirs{$chr};
		@p = inside(@np) ?? @np !! @p;
	}
	to-num2(|@p).base(16)
};

say join "", @part2;
