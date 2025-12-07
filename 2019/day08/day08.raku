my @test = (1,2,3,4,5,6,7,8,9,0,1,2);
my @real = "../inputs/day08-real.txt".IO.slurp;

say @test.batch(6);

