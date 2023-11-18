use crate::intcode::{IntCode, OutputMessage};
use itertools::Itertools;
use std::vec::Vec;

fn part1_impl(code: &str) -> (i64, Vec<i64>) {
    let mut amps = (0..5)
        .map(|_| IntCode::new_from_str(code))
        .collect::<Vec<_>>();

    (0..5)
        .permutations(5)
        .map(|perm| {
            for (i, amp) in amps.iter_mut().enumerate() {
                amp.reset();
                amp.run();
                amp.input(perm[i]);
            }

            amps[0].input(0);

            for (amp1, amp2) in amps.iter().tuple_windows() {
                amp2.input(amp1.output_value());
            }

            let result = amps[4].output_value();

            for amp in amps.iter_mut() {
                amp.output_halt();
            }

            (result, perm)
        })
        .max()
        .unwrap()
}

pub fn part1() {
    // let tests = include_str!("../inputs/day07-test.txt")
    //     .trim()
    //     .split("\n")
    //     .take(3);

    // for (i, test) in tests.enumerate() {
    //     let (val, perm) = part1_impl(test);

    //     println!("Part 1 test {}: {} ({:?})", i, val, perm);
    // }

    let real = include_str!("../inputs/day07-real.txt");
    let (val, _) = part1_impl(real);

    println!("Part 1: {}", val);
}

fn part2_impl(code: &str) -> (i64, Vec<i64>) {
    let mut amps = (0..5)
        .map(|_| IntCode::new_from_str(code))
        .collect::<Vec<_>>();

    (5..10)
        .permutations(5)
        .map(|perm| {
            for (i, amp) in amps.iter_mut().enumerate() {
                amp.reset();
                amp.run();
                amp.input(perm[i]);
            }

            amps[0].input(0);

            let mut result: Option<i64> = None;

            loop {
                for (amp1, amp2) in amps.iter().tuple_windows() {
                    let out = amp1.output();

                    match out {
                        OutputMessage::Value(v) => amp2.input(v),
                        OutputMessage::Halt => (),
                    }
                }

                match amps[4].output() {
                    OutputMessage::Value(v) => {
                        result = Some(v);
                        amps[0].input(v);
                    }
                    OutputMessage::Halt => break (result.unwrap(), perm),
                }
            }
        })
        .max()
        .unwrap()
}

pub fn part2() {
    // let tests = include_str!("../inputs/day07-test.txt")
    //     .trim()
    //     .split("\n")
    //     .skip(3);

    // for (i, test) in tests.enumerate() {
    //     let (val, perm) = part2_impl(test);

    //     println!("Part 2 test {}: {} ({:?})", i, val, perm);
    // }

    let real = include_str!("../inputs/day07-real.txt");
    let (val, _) = part2_impl(real);
    println!("Part 2: {}", val);
}
