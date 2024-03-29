use std::fs;

// X for Rock, Y for Paper, and Z for Scissors
// (1 for Rock, 2 for Paper, and 3 for Scissors)
// plus the score for the outcome of the round
// (0 if you lost, 3 if the round was a draw, and 6 if you won).

fn score(x: &[char]) -> i32 {
    match x {
        &['A', 'X'] => 1 + 3,
        &['B', 'X'] => 1,
        &['C', 'X'] => 1 + 6,
        &['A', 'Y'] => 2 + 6,
        &['B', 'Y'] => 2 + 3,
        &['C', 'Y'] => 2,
        &['A', 'Z'] => 3,
        &['B', 'Z'] => 3 + 6,
        &['C', 'Z'] => 3 + 3,
        _ => unreachable!(),
    }
}
// X means you need to lose, Y means you need to end the round in a draw,
// and Z means you need to win
fn score2(x: &[char]) -> i32 {
    match x {
        &['A', 'X'] => 3 + 0,
        &['B', 'X'] => 1 + 0,
        &['C', 'X'] => 2 + 0,
        &['A', 'Y'] => 1 + 3,
        &['B', 'Y'] => 2 + 3,
        &['C', 'Y'] => 3 + 3,
        &['A', 'Z'] => 2 + 6,
        &['B', 'Z'] => 3 + 6,
        &['C', 'Z'] => 1 + 6,
        y => unreachable!("no match {:?}", y),
    }
}

pub fn run() {
    println!("day02");

    let rounds: Vec<char> = fs::read_to_string("data/day02.txt")
        .unwrap()
        .chars()
        .filter(|x| char::is_alphabetic(*x))
        .collect();
    let res: (i32, i32) = rounds
        .chunks(2)
        .fold((0, 0), |acc, x| (acc.0 + score(x), acc.1 + score2(x)));
    println!("PART 1: {}", res.0);
    println!("PART 2: {}", res.1);
}
