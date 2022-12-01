use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn count_num(s: &str) -> (i32, i32) {
    let mut h = HashMap::new();
    s.chars().for_each(|c| *h.entry(c).or_insert(0) += 1);
    let mut x = 0;
    let mut y = 0;
    if h.values().any(|&x| x == 2) {
        x += 1;
    }
    if h.values().any(|&x| x == 3) {
        y += 1;
    }
    (x, y)
}

pub fn run() {
    println!("day02");
    let ls: Vec<String> = File::open("data/day02.txt")
        .map(|x| BufReader::new(x).lines())
        .unwrap()
        .map(std::result::Result::unwrap)
        .collect();
    let (a, b) = ls.iter().fold((0, 0), |(x0, y0), s| {
        let (x, y) = count_num(s);
        (x0 + x, y0 + y)
    });
    println!("PART 1: {}", a * b);
    let mut res: String = String::from("");
    let mut max_common = 0;
    for s1 in &ls {
        for s2 in &ls {
            if s1 == s2 {
                continue;
            }
            let common_s: String = s1
                .chars()
                .zip(s2.chars())
                .filter(|(x, y)| x == y)
                .map(|(x, y)| x)
                .collect();
            let common = common_s.len();
            if common > max_common {
                max_common = common;
                res = common_s;
            }
        }
    }
    println!("PART 2: {}", res);
}
