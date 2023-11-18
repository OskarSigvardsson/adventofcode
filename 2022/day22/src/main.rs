use std::fs::File;
use std::io::{BufReader, BufRead};
// use itertools::Itertools;

enum Tile {
    Path,
    Wall,
    Empty,
}

fn main() {
    let file = File::open("test.txt").unwrap();
    let lines = BufReader::new(file)
        .lines()
        .map(|line| line.unwrap());


}
