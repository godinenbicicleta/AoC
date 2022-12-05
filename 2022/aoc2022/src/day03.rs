use std::fs;

pub fn score(c: i32) -> i32 {
    match c {
        92.. => c - 96,
        _ => c - 38,
    }
}

pub fn score1(line: &str) -> i32 {
    for c1 in line.chars().take(line.len() / 2) {
        for c2 in line.chars().skip(line.len() / 2) {
            if c1 == c2 {
                return score(c1 as i32);
            }
        }
    }
    panic!("no match in line {}", line);
}
pub fn score2(line: &[&str]) -> i32 {
    for c1 in line[0].chars() {
        for c2 in line[1].chars() {
            if c1 != c2 {
                continue;
            }
            for c3 in line[2].chars() {
                if c2 == c3 {
                    return score(c1 as i32);
                }
            }
        }
    }
    panic!("no match in line {}", line[0]);
}
pub fn run() {
    println!("day03");
    let s = fs::read_to_string("data/day03.txt").unwrap();
    let p1: i32 = s.lines().map(|line| score1(line)).sum();
    let p2: i32 = s
        .lines()
        .collect::<Vec<&str>>()
        .chunks(3)
        .map(|x| score2(x))
        .sum();
    println!("PART 1: {}", p1);
    println!("PART 1: {}", p2);
}
