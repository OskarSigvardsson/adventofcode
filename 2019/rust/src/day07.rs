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
                amp.ignore_wants_input(true);
                amp.run();
                amp.input(perm[i]);
            }

            amps[0].input(0);

            for (amp1, amp2) in amps.iter().tuple_windows() {
                amp2.input(amp1.output_value().unwrap());
            }

            let result = amps[4].output_value().unwrap();

            for amp in amps.iter_mut() {
                amp.output_halt().unwrap();
            }

            (result, perm)
        })
        .max()
        .unwrap()
}

#[test]
fn part1_test() {
    let tests = include_str!("../inputs/day07-test.txt")
        .trim()
        .split("\n")
        .take(3);

    let result = tests
        .enumerate()
        .map(|(i, test)| {
            let (val, perm) = part1_impl(test);

            println!("Part 1 test {}: {} ({:?})", i, val, perm);

            perm
        })
        .collect::<Vec<_>>();

    assert_eq!(result[0], vec![4, 3, 2, 1, 0]);
    assert_eq!(result[1], vec![0, 1, 2, 3, 4]);
    assert_eq!(result[2], vec![1, 0, 4, 3, 2]);
}

pub fn part1() {
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
                amp.ignore_wants_input(true);
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
                        OutputMessage::WantsInput => panic!(),
                        OutputMessage::Halt => (),
                    }
                }

                match amps[4].output() {
                    OutputMessage::Value(v) => {
                        result = Some(v);
                        amps[0].input(v);
                    }
                    OutputMessage::Halt => break (result.unwrap(), perm),
                    OutputMessage::WantsInput => panic!(),
                }
            }
        })
        .max()
        .unwrap()
}

#[test]
fn part2_test() {
    let tests = include_str!("../inputs/day07-test.txt")
        .trim()
        .split("\n")
        .skip(3);

    let result = tests
        .enumerate()
        .map(|(i, test)| {
            let (val, perm) = part2_impl(test);

            println!("Part 2 test {}: {} ({:?})", i, val, perm);

            perm
        })
        .collect::<Vec<_>>();

    assert_eq!(result[0], vec![9, 8, 7, 6, 5]);
    assert_eq!(result[1], vec![9, 7, 8, 5, 6]);
}

pub fn part2() {
    let real = include_str!("../inputs/day07-real.txt");
    let (val, _) = part2_impl(real);
    println!("Part 2: {}", val);
}
