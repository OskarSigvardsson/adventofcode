use md5;

fn part1(prefix: &str) -> String {
    (0..i64::MAX)
        .map(|i| format!("{:x}", md5::compute(format!("{}{}", &prefix, i))))
        .filter(|s| s.starts_with("00000"))
        .take(8)
        .fold(String::from(""), |mut a, b| {
            a.push(b.chars().nth(5).unwrap());
            a
        })
}

fn part2(prefix: &str) -> String {
	let mut pass = vec!['_'; 8];

	for i in 0.. {
		let hash = format!("{:x}", md5::compute(format!("{}{}", &prefix, i)));

		if hash.starts_with("00000") {
            let pos = hash.chars().nth(5).unwrap().to_digit(16).unwrap() as usize;
            let chr = hash.chars().nth(6).unwrap();

			if pos < pass.len() && pass[pos] == '_'{
				pass[pos] = chr;

				if !pass.iter().any(|c| *c == '_') { break; }
			}
			println!("{} {}", pass.iter().collect::<String>(), hash);
		}
	}

	pass.into_iter().collect()
}

fn main() {
    //println!("Part 1: {}", part1("abc"));
    println!("Part 2: {}", part2("reyedfim"));
}
