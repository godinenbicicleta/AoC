use std::collections::HashSet;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::str::FromStr;

#[allow(clippy::maybe_infinite_iter)]
pub fn run() {
    println!("day01");
    let int_lines: Vec<i32> = File::open("data/day01.txt")
        .map(|x| {
            BufReader::new(x)
                .lines()
                .map(|x| i32::from_str(&x.unwrap()).unwrap())
                .collect()
        })
        .unwrap();
    let res: i32 = int_lines.iter().sum();

    println!("PART 1: {}", res);
    let mut seen: HashSet<i32> = HashSet::new();
    let res2: i32 = int_lines
        .iter()
        .cycle()
        .scan(0, |state, &x| {
            *state += x;
            Some(*state)
        })
        .find(|&x| {
            if seen.contains(&x) {
                true
            } else {
                seen.insert(x);
                false
            }
        })
        .unwrap();
    println!("PART 2: {}", res2);
}
