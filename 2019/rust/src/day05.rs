use crate::intcode::{IntCode, OutputMessage};

pub fn part1() {
    let mut test = IntCode::new_from_str(include_str!("../inputs/day05-real.txt"));
    test.run();
    test.input(1);
    let mut val: i64 = 0;

    loop {
        match test.output() {
            OutputMessage::Value(v) => {
                if val != 0 {
                    panic!("Error, prev val should be 0");
                }
                val = v
            }
            OutputMessage::Halt => break,
        }
    }
    if val == 0 {
        panic!("Output value should be non-zero!")
    }
    println!("Part 1: {}", val);
}

#[test]
fn part2_test() {
    let mut test = IntCode::new_from_str(include_str!("../inputs/day05-test.txt"));
    test.debug(false);

    for i in 0..20 {
        test.reset();
        test.run();
        test.input(i);

        let o1 = test.output();
        let o2 = test.output();

        let expected = if i < 8 {
            999
        } else if i == 8 {
            1000
        } else {
            1001
        };

        assert_eq!(o1, OutputMessage::Value(expected));
        assert_eq!(o2, OutputMessage::Halt);
    }
}

pub fn part2() {
    let mut real = IntCode::new_from_str(include_str!("../inputs/day05-real.txt"));
    real.debug(false);
    real.reset();
    real.run();
    real.input(5);

    match real.output() {
        OutputMessage::Value(v) => println!("Part 2: {}", v),
        OutputMessage::Halt => panic!("Unexpected halt!"),
    }

    match real.output() {
        OutputMessage::Value(_) => panic!("Unexpected value!"),
        OutputMessage::Halt => (),
    }
}
