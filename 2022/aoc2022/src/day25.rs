use std::fs;

use std::iter;

fn to_n(v: &[char]) -> i64 {
    let s1: String = v.iter().collect();
    to_num(&s1)
}

fn to_num(s: &str) -> i64 {
    let mut n = 0;
    let mut curr = 1;
    for (c, num) in s.chars().rev().zip(iter::repeat_with(|| {
        let temp = curr;
        curr *= 5;
        temp
    })) {
        n += match c {
            '2' => 2 * num,
            '1' => num,
            '-' => -num,
            '=' => -2 * num,
            '0' => 0,
            _ => {
                println!("{c}");
                unreachable!()
            }
        }
    }
    n
}

fn to_max(u: usize) -> i64 {
    let mut res = 0;
    for p in 0..u {
        res += 2 * i64::pow(5, p as u32);
    }
    res
}
fn solve(v: Vec<char>, goal: i64) -> Vec<char> {
    let mut res = v;
    let mut ix = 1;
    while to_n(&res) != goal && ix < res.len() {
        let mut o = res.clone();
        if to_n(&o) > goal {
            o[ix] = '-';
            if to_n(&o) < goal {
                if to_n(&o) + to_max(res.len() - ix - 1) < goal {
                    o[ix] = '0'
                }
                res = o;
                ix += 1;
                continue;
            } else {
                o[ix] = '=';
                if to_n(&o) + to_max(res.len() - ix - 1) < goal {
                    o[ix] = '-'
                }
                res = o;
                ix += 1;
                continue;
            }
        }
        o[ix] = '1';
        if to_n(&o) > goal && to_n(&o) - to_max(res.len() - ix - 1) > goal {
            o[ix] = '0';
            res = o;
            ix += 1;
            continue;
        } else if to_n(&o) > goal {
            res = o;
            ix += 1;
            continue;
        } else {
            o[ix] = '2';
            if to_n(&o) - to_max(res.len() - ix - 1) > goal {
                o[ix] = '1';
            }
            res = o;
            ix += 1;
            continue;
        }
    }
    res
}

fn to_string(goal: i64) -> String {
    let mut size = 0;
    let mut current = 1;
    loop {
        if current >= goal || current * 2 >= goal {
            break;
        }
        size += 1;
        current = i64::pow(5, size);
    }

    let mut res = Vec::new();
    for _ in 0..=(size as usize) {
        res.push('0');
    }
    if i64::pow(5, size) > goal {
        res[0] = '1';
    } else {
        res[0] = '2';
    }

    let res = solve(res, goal);

    res.iter().collect()
}

pub fn run() {
    println!("day25");
    let s = fs::read_to_string("data/day25.txt").unwrap();

    let mut total = 0;
    for line in s.lines() {
        let num = to_num(line);
        total += num;
    }
    println!("{total}");
    let res = to_string(total);
    println!("{res}");
}
