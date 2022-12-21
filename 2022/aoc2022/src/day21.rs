use std::cmp::Ordering;
use std::collections::HashMap;
use std::fs;
use std::str::FromStr;

#[derive(Debug, Clone)]
enum Op {
    Num(i128),
    Add(String, String),
    Mul(String, String),
    Sub(String, String),
    Div(String, String),
    Compare(String, String),
}

fn evaluate(key: &str, d: &HashMap<String, Op>) -> i128 {
    match d.get(key).unwrap() {
        Op::Num(n) => *n,
        Op::Add(left, right) => evaluate(left, d) + evaluate(right, d),
        Op::Mul(left, right) => evaluate(left, d) * evaluate(right, d),
        Op::Div(left, right) => evaluate(left, d) / evaluate(right, d),
        Op::Sub(left, right) => evaluate(left, d) - evaluate(right, d),
        Op::Compare(left, right) => {
            let left = evaluate(left, d);
            let right = evaluate(right, d);
            match left.cmp(&right) {
                Ordering::Less => -1,
                Ordering::Equal => 0,
                Ordering::Greater => 1,
            }
        }
    }
}

pub fn run() {
    println!("day21");
    let s = fs::read_to_string("data/day21.txt").unwrap();
    let mut d = HashMap::new();
    let mut p2_root = Op::Num(1);
    for line in s.lines() {
        let (key, raw_v) = line.split_once(": ").unwrap();
        if let Some(num) = i128::from_str(raw_v).ok() {
            d.insert(key.to_string(), Op::Num(num));
            continue;
        }
        let mut splitted = raw_v.split_whitespace();
        let left = splitted.next().unwrap().to_string();
        let op = splitted.next().unwrap();
        let right = splitted.next().unwrap().to_string();
        if key == "root" {
            p2_root = Op::Compare(left.to_string(), right.to_string());
        }
        match op {
            "+" => d.insert(key.to_string(), Op::Add(left, right)),
            "-" => d.insert(key.to_string(), Op::Sub(left, right)),
            "*" => d.insert(key.to_string(), Op::Mul(left, right)),
            "/" => d.insert(key.to_string(), Op::Div(left, right)),
            _ => {
                unreachable!()
            }
        };
    }
    println!("{}", evaluate("root", &d));
    d.insert("root".to_string(), p2_root.clone());
    let mut minx: i128 = 0;
    let mut maxx: i128 = 72664227897438;
    while minx <= maxx {
        let mid = (minx + maxx) / 2;
        d.insert("humn".to_string(), Op::Num(mid));
        match evaluate("root", &d) {
            0 => {
                for i in mid - 10..mid + 10 {
                    d.insert("humn".to_string(), Op::Num(i));
                    if evaluate("root", &d) == 0 {
                        println!("{}", i);
                    }
                }
                break;
            }
            -1 => maxx = mid - 1,
            1 => minx = mid + 1,
            _ => unreachable!(),
        }
    }
}
