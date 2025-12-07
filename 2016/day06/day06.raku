my @lines = "../inputs/day06-real.txt".IO.lines.map(*.comb); 
my @bags = ([Z] @lines).map(*.Bag);

say @bags.map(*.antipairs.max).map(*.value).join('');
say @bags.map(*.antipairs.min).map(*.value).join('');
