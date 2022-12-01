use std::fs::File;
use std::io::{BufRead, BufReader};
use std::str::FromStr;

pub fn run() {
    println!("day01");
    let f = File::open("data/day01.txt").unwrap();
    let mut energies: Vec<i32> = vec![0];
    BufReader::new(f).lines().fold(&mut energies, |acc, line| {
        if let Ok(num) = i32::from_str(&line.unwrap()) {
            let s = acc.len();
            acc[s - 1] += num;
        } else {
            acc.push(0)
        }
        acc
    });
    energies.sort_by(|x, y| y.cmp(&x));
    let p1: i32 = energies[0];
    let p2: i32 = energies[..3].iter().sum();

    println!("PART 1: {}", p1);
    println!("PART 2: {}", p2);
}
