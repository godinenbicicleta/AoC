use std::collections::VecDeque;
use std::fs;
use std::str::FromStr;

#[allow(unreachable_code)]
fn right_order(line1: &str, line2: &str) -> bool {
    let mut left: VecDeque<_> = line1.chars().collect();
    let mut right: VecDeque<_> = line2.chars().collect();
    loop {
        let c1 = left.pop_front().unwrap();
        let c2 = right.pop_front().unwrap();
        match (c1, c2) {
            (',', ',') => continue,
            // both values are integers
            (n1, n2) if n1.is_ascii_digit() && n2.is_ascii_digit() => {
                let left_num = if *left.front().unwrap() == '0' {
                    u32::from_str(&[n1, left.pop_front().unwrap()].iter().collect::<String>())
                        .unwrap()
                } else {
                    n1.to_digit(10).unwrap()
                };
                let right_num = if *right.front().unwrap() == '0' {
                    u32::from_str(&[n2, right.pop_front().unwrap()].iter().collect::<String>())
                        .unwrap()
                } else {
                    n2.to_digit(10).unwrap()
                };
                if left_num < right_num {
                    return true;
                } else if left_num > right_num {
                    return false;
                } else {
                    continue;
                }
            }
            // both values are lists
            (']', ']') => continue,
            ('[', '[') => continue,
            //   left runs out of items first
            (']', _) => return true,
            //   right runs out of items first
            (_, ']') => return false,
            // mixed
            ('[', num) => {
                left.push_front('[');
                if *right.front().unwrap() == '0' {
                    let _ = right.pop_front().unwrap();
                    right.push_front(']');
                    right.push_front('0');
                    right.push_front(num);
                    right.push_front('[');
                } else {
                    right.push_front(']');
                    right.push_front(num);
                    right.push_front('[');
                }
            }
            (num, '[') => {
                right.push_front('[');
                if *left.front().unwrap() == '0' {
                    let _ = left.pop_front().unwrap();
                    left.push_front(']');
                    left.push_front('0');
                    left.push_front(num);
                    left.push_front('[');
                } else {
                    left.push_front(']');
                    left.push_front(num);
                    left.push_front('[');
                }
            }
            _ => unreachable!(),
        }
    }
}

fn find_index(start: u32, s: &str, divider: &str) -> u32 {
    let mut ix = start;

    for pair in s.split("\n\n") {
        let mut lines = pair.lines();
        let line1 = lines.next().unwrap();
        let line2 = lines.next().unwrap();
        if right_order(line1, divider) {
            ix += 1;
        }
        if right_order(line2, divider) {
            ix += 1;
        }
    }
    ix
}

pub fn run() {
    let s = fs::read_to_string("data/day13.txt").unwrap();

    let mut p1 = 0;
    for (ix, pair) in s.split("\n\n").enumerate() {
        let mut lines = pair.lines();
        let line1 = lines.next().unwrap();
        let line2 = lines.next().unwrap();
        if right_order(line1, line2) {
            p1 += ix + 1;
        }
    }
    let d1 = "[[2]]";
    let d2 = "[[6]]";
    let d1x = find_index(1, &s, d1);
    let d2x = find_index(2, &s, d2); // starts at 2 because greater than d1
    println!("PART 1: {}", p1);
    println!("PART 2: {}", d1x * d2x);
}
