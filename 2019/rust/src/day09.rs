use crate::intcode::{IntCode, OutputMessage};

#[test]
fn part1_test() {
    let results = include_str!("../inputs/day09-test.txt")
        .trim()
        .split("\n")
        .collect::<Vec<_>>();

    dbg!(&results);
    let code1 = results[0]
        .split(",")
        .map(|s| s.trim().parse::<i64>().unwrap())
        .collect::<Vec<_>>();

    let mut c1 = IntCode::new(code1.clone());
    //c1.debug(true);
    c1.run();

    assert_eq!(code1, c1.collect_output());

    let mut c2 = IntCode::new_from_str(results[1]);
    c2.run();
    assert_eq!(16, c2.output_value().to_string().len());

    let code3 = results[2]
        .split(",")
        .map(|s| s.trim().parse::<i64>().unwrap())
        .collect::<Vec<_>>();
    let mut c3 = IntCode::new(code3.clone());
	c3.run();

	assert_eq!(code3[1], c3.output_value());
}

pub fn part1() {
	let mut ic = IntCode::new_from_str(include_str!("../inputs/day09-real.txt"));
	ic.run();
	ic.input(1);

	loop {
		match ic.output() {
			OutputMessage::Value(v) => println!("Part 1: {v}"),
			OutputMessage::Halt => break,
		}
	}
}

pub fn part2() {
	let mut ic = IntCode::new_from_str(include_str!("../inputs/day09-real.txt"));
	ic.run();
	ic.input(2);

	loop {
		match ic.output() {
			OutputMessage::Value(v) => println!("Part 2: {v}"),
			OutputMessage::Halt => break,
		}
	}
}
