use crate::intcode::IntCode;

pub fn part1() {
    // let mut test = IntCode::new_from_str(include_str!("../inputs/day02-test.txt"));
    // test.run_to_halt();
    // println!("Part 1 test: {}", test.load(0));

    let mut real = IntCode::new_from_str(include_str!("../inputs/day02-real.txt"));
    real.store(1, 12);
    real.store(2, 2);
    real.run_to_halt();
    println!("Part 1: {}", real.load(0));
}

pub fn part2() {
    let mut real = IntCode::new_from_str(include_str!("../inputs/day02-real.txt"));

    'outer: for x in 0..99 {
        for y in 0..99 {
            real.store(1, x);
            real.store(2, y);
            real.run_to_halt();

            if real.load(0) == 19690720 {
                println!("Part 2: {}", x * 100 + y);
                break 'outer;
            } else {
                real.reset();
            }
        }
    }
}
