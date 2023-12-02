use std::collections::{HashMap, HashSet};
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::str::FromStr;
#[derive(Debug, Clone, Copy, Eq, Hash, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

struct Claim {
    id: i32,
    ps: HashSet<Point>,
}

fn parse_line(x: &str) -> Claim {
    // #1 @ 604,100: 17x27
    let mut it = x.strip_prefix('#').unwrap().split_whitespace();
    let id = i32::from_str(it.next().unwrap()).unwrap();
    it.next(); // discard @
    let xy: Vec<i32> = it
        .next()
        .unwrap()
        .strip_suffix(':')
        .unwrap()
        .split(',')
        .map(|x| i32::from_str(x).unwrap())
        .collect();
    let wh: Vec<i32> = it
        .next()
        .unwrap()
        .split('x')
        .map(|x| i32::from_str(x).unwrap())
        .collect();
    let mut points = HashSet::new();
    for x in xy[0]..(xy[0] + wh[0]) {
        for y in xy[1]..(xy[1] + wh[1]) {
            points.insert(Point { x, y });
        }
    }

    Claim { id, ps: points }
}

pub fn run() {
    println!("day03");
    // #1 @ 604,100: 17x27
    let f = File::open("data/day03.txt").unwrap();
    let claims: Vec<Claim> = BufReader::new(f)
        .lines()
        .map(|x| parse_line(&x.unwrap()))
        .collect();

    let mut points: HashMap<Point, i32> = HashMap::new();
    for claim in &claims {
        for &point in &(claim.ps) {
            *points.entry(point).or_insert(0) += 1;
        }
    }
    let p1 = points.values().filter(|&x| *x > 1).count();
    println!("PART 1: {}", p1);
    let p2 = claims.iter().find(|x| {
        claims
            .iter()
            .filter(|c| c.id != x.id)
            .all(|c| c.ps.is_disjoint(&x.ps))
    });
    println!("PART 2: {}", p2.unwrap().id);
}
