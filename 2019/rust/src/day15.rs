use std::collections::HashMap;

use crate::intcode::*;

enum Tile {
	Wall,
	Floor,
	Oxygen,
}

pub fn part1() {
	let mut ic = IntCode::new_from_str(include_str!("../inputs/day15-real.txt"));

	let field = HashMap::<(i64, i64), Tile>::new();
	let path = vec![(0 as i64, 0 as i64)];
}
