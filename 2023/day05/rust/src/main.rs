use rayon::prelude::*;
use regex::Regex;
use std::fs;

fn apply_maps(seed: i64, maps: &Vec<Vec<(i64, i64, i64)>>) -> i64 {
    let mut n = seed;

    for map in maps.iter() {
        for &(src, dest, count) in map.iter() {
            if dest <= n && n < dest + count {
                n = src + (n - dest);
                break;
            }
        }
    }

    n
}

fn main() {
    let file = fs::read_to_string("../../inputs/day05-real.txt").unwrap();
    let file = file.split("\n").collect::<Vec<_>>();
    let seeds = Regex::new(r"\d+")
        .unwrap()
        .find_iter(file[0])
        .map(|s| s.as_str().parse::<i64>().unwrap())
        .collect::<Vec<_>>();

    let re = Regex::new(r"(\d+) (\d+) (\d+)").unwrap();
    let mut maps = vec![];
    let mut curr_map = vec![];

    for line in file.iter().skip(2) {
        if let Some(cs) = re.captures(line) {
            let cs = cs
                .iter()
                .skip(1)
                .map(|s| s.unwrap().as_str().parse::<i64>().unwrap())
                .collect::<Vec<_>>();

            curr_map.push((cs[0], cs[1], cs[2]));
        } else if line.trim() == "" {
            maps.push(curr_map);
            curr_map = vec![];
        }
    }

    let part1 = seeds.iter().map(|&s| apply_maps(s, &maps)).min().unwrap();

    println!("Part 1: {part1}");

    let part2 = seeds
        .chunks(2)
        .map(|range| {
            let (beg, count) = (range[0], range[1]);

            (beg..(beg + count))
                .into_par_iter()
                .map(|s| apply_maps(s, &maps))
                .min()
                .unwrap()
        })
        .min()
        .unwrap();

	println!("Part 2: {part2}");
}
