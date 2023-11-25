use crate::intcode::*;

use num_complex::Complex;
use std::collections::HashMap;

fn paint(initial_color: u8) -> HashMap<Complex<i64>, u8> {
    let mut robot = IntCode::new_from_str(include_str!("../inputs/day11-real.txt"));
    robot.run();

    let left = Complex::<i64> { re: 0, im: 1 };
    let right = Complex::<i64> { re: 0, im: -1 };
    let dirs = [left, right];

    let mut dir = Complex::<i64> { re: 0, im: 1 };
    let mut pos = Complex::<i64> { re: 0, im: 0 };

    let mut panels = HashMap::<Complex<i64>, u8>::new();

    panels.insert(pos, initial_color);

    loop {
        let panel = *panels.get(&pos).unwrap_or(&0);

        robot.input(panel as i64);

        match robot.output() {
            OutputMessage::Value(color) => {
                assert!(color == 0 || color == 1);

                panels.insert(pos, color as u8);

                let turn = dirs[robot.output_value().unwrap() as usize];

                dir *= turn;
                pos += dir;
            }

            OutputMessage::WantsInput => (),

            OutputMessage::Halt => {
                break panels;
            }
        }
    }
}

pub fn part1() {
    let panels = paint(0);
    println!("Part 1: {}", panels.len());
}

pub fn part2() {
    println!("Part 2:");

    let panels = paint(1);
    let min_re = panels.keys().map(|k| k.re).min().unwrap();
    let max_re = panels.keys().map(|k| k.re).max().unwrap();
    let min_im = panels.keys().map(|k| k.im).min().unwrap();
    let max_im = panels.keys().map(|k| k.im).max().unwrap();

    for im in (min_im..=max_im).rev() {
        for re in min_re..max_re {
            let pos = Complex::<i64> { re, im };

            print!(
                "{}",
                if 1 == *panels.get(&pos).unwrap_or(&0) {
                    "#"
                } else {
                    " "
                }
            );
        }
        println!();
    }
}
