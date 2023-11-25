use crate::intcode::*;

use std::collections::HashMap;

#[derive(PartialEq, Eq)]
#[repr(u8)]
enum Tile {
    Empty = 0,
    Wall = 1,
    Block = 2,
    Paddle = 3,
    Ball = 4,
}

impl Tile {
    fn from(v: i64) -> Self {
        match v {
            0 => Self::Empty,
            1 => Self::Wall,
            2 => Self::Block,
            3 => Self::Paddle,
            4 => Self::Ball,
            _ => panic!("unknown tile type"),
        }
    }
}

pub fn part1() {
    let mut game = IntCode::new_from_str(include_str!("../inputs/day13-real.txt"));
    game.run();

    let mut screen = HashMap::<(i64, i64), Tile>::new();

    loop {
        match game.output() {
            OutputMessage::Halt => break,
            OutputMessage::WantsInput => panic!("unexpected wants input"),
            OutputMessage::Value(x) => {
                let y = game.output_value().unwrap();
                let t = Tile::from(game.output_value().unwrap());
                screen.insert((x, y), t);
            }
        }
    }

    let blocks = screen.values().filter(|t| **t == Tile::Block).count();
    println!("Part 1: {}", blocks);
}

// fn draw_screen(screen: &HashMap<(i64, i64), Tile>) {
//     let minx = screen.keys().map(|k| k.0).min().unwrap_or(0);
//     let maxx = screen.keys().map(|k| k.0).max().unwrap_or(0);
//     let miny = screen.keys().map(|k| k.1).min().unwrap_or(0);
//     let maxy = screen.keys().map(|k| k.1).max().unwrap_or(0);

//     for y in miny..=maxy {
//         for x in minx..=maxx {
//             let chr = match screen.get(&(x, y)).unwrap_or(&Tile::Empty) {
//                 Tile::Empty => " ",
//                 Tile::Wall => "#",
//                 Tile::Block => "x",
//                 Tile::Paddle => "-",
//                 Tile::Ball => "o",
//             };

//             print!("{}", chr);
//         }

//         println!();
//     }
// }

pub fn part2() {
    let mut game = IntCode::new_from_str(include_str!("../inputs/day13-real.txt"));
    game.store(0, 2);
    game.run();

    let mut screen = HashMap::<(i64, i64), Tile>::new();
    let mut score = 0;
    // let mut input = String::new();
    let mut ball = 0;
    let mut paddle = 0;

    'outer: loop {
        loop {
            match game.try_output() {
                Some(v) => match v {
                    OutputMessage::Halt => {
                        break 'outer;
                    }
                    OutputMessage::Value(x) => {
                        let y = game.output_value().unwrap();

                        if x == -1 {
                            assert_eq!(y, 0);
                            score = game.output_value().unwrap();
                        } else {
                            let tile = Tile::from(game.output_value().unwrap());

                            match tile {
                                Tile::Paddle => paddle = x,
                                Tile::Ball => ball = x,
                                _ => (),
                            };

                            screen.insert((x, y), tile);
                        }
                    }
                    OutputMessage::WantsInput => {
                        break;
                    }
                },
                None => {}
            };
        }

        //draw_screen(&screen);
        // println!("Score: {score}");

        if paddle < ball {
            game.input(1);
        } else if paddle > ball {
            game.input(-1);
        } else {
            game.input(0);
        }

        // input.clear();
        // io::stdin().read_line(&mut input).unwrap();
    }
    println!("Part 2: {score}");
}
