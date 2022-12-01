# use Math::Matrix;

my @ingredients = [(-1, -2, 6, 3, 8), (2, 3, -2, -1, 3)];
my @mat = ($_[0..^*-1] for @ingredients);

say @mat;

# say $ingredients;

sub matmul(@m1, @m2) {
	my ($r1, $c1) = @m1.elems, @m1[0].elems;
	my ($r2, $c2) = @m2.elems, @m2[0].elems;

	when $c1 != $r2 { die "mismatched matrix dimensions $c1 and $r2" }
	
	my @result;
	
	for ^$r1 X ^$c2 -> ($r, $c) {
		for ^$c1 -> $i {
			@result[$r][$c] += @m1[$r][$i] * @m2[$i][$c];
		}
	}

	@result
}

sub test($vals, $sum, @prefix) {
	if $vals == 1 {
		my @list = [[|@prefix, $sum],];

		my @m = matmul(@list, @mat);

		say @list, " -> ", @m, " -> ", [*] @m[0].list;
		
	} else {
		(0..$sum).map({ test($vals-1, $sum - $_, [|@prefix, $_]) }).sum
	}
}

my @a = [1,  1,  1,   1],
        [2,  4,  8,  16],
        [3,  9, 27,  81],
        [4, 16, 64, 256];

my @b = [  4  , -3  ,  4/3,  -1/4 ],
        [-13/3, 19/4, -7/3,  11/24],
        [  3/2, -2  ,  7/6,  -1/4 ],
        [ -1/6,  1/4, -1/6,   1/24];

test(2, 100, []);

# my @a = [1, 2],
#         [3, 4];

# my @b = [5, 6],
#         [7, 8];

.say for matmul(@a, @b);

