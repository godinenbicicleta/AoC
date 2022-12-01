use std::fs::File;
use std::io::{BufRead, BufReader};
use std::str::FromStr;
#[derive(Debug, Clone, Copy)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Debug, Clone, Copy)]
struct Claim<'a> {
    id: i32,
    ps: &'a Vec<Point>,
}

fn parse_line(x: String) -> Claim {
    let mut it = x.strip_prefix("#").unwrap().split_whitespace();
    let id = i32::from_str(it.next().unwrap()).unwrap();
    let xy: Vec<i32> = it
        .next()
        .unwrap()
        .strip_suffix(":")
        .unwrap()
        .split(",")
        .map(|x| i32::from_str(x).unwrap())
        .collect();
    let wh: Vec<i32> = it
        .next()
        .unwrap()
        .split(",")
        .map(|x| i32::from_str(x).unwrap())
        .collect();
    let mut points = Vec::with_capacity((wh[0] * wh[0]) as usize);
    for x in xy[0]..(xy[0] + wh[0] + 1) {
        for y in xy[0]..(xy[1] + wh[1] + 1) {
            points.push(Point { x, y })
        }
    }

    Claim { id, ps: &points }
}

pub fn run() {
    println!("day03");
    // #1 @ 604,100: 17x27
    let f = File::open("data/day03.txt").unwrap();
    let ls = BufReader::new(f).lines().map(|x| parse_line(x.unwrap()));
}
