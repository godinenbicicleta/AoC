use std::collections::HashSet;
use std::fs;
use std::str::FromStr;
#[derive(Debug, Clone, Copy, Eq, PartialEq, Hash)]
struct Point {
    x: i32,
    y: i32,
    z: i32,
}

fn to_points(p: Point) -> HashSet<Point> {
    let mut s = HashSet::new();
    for x in [p.x - 1, p.x] {
        for y in [p.y - 1, p.y] {
            for z in [p.z - 1, p.z] {
                s.insert(Point { x, y, z });
            }
        }
    }
    s
}
pub fn run() {
    println!("day18");

    let s = fs::read_to_string("data/day18_test.txt").unwrap();
    let mut points = Vec::new();
    for line in s.lines() {
        let mut coords = line.split(",").map(|x| i32::from_str(x).unwrap());
        let x = coords.next().unwrap();
        let y = coords.next().unwrap();
        let z = coords.next().unwrap();
        points.push(Point { x, y, z })
    }
    let mut part1 = points.len() * 6;
    let ps: Vec<_> = points.iter().map(|x| to_points(*x)).collect();
    for i in 0..points.len() - 1 {
        for j in i..points.len() {
            if ps[i].intersection(&ps[j]).count() == 4 {
                part1 -= 2;
            }
        }
    }
    println!("PART 1: {}", part1);
    let existing_points = points.iter().map(|p| *p).collect::<HashSet<Point>>();
    let mut all_points: HashSet<Point> = HashSet::new();
    let maxz = points.iter().map(|x| x.z).max().unwrap();
    let minz = points.iter().map(|x| x.z).min().unwrap();
    let maxy = points.iter().map(|x| x.y).max().unwrap();
    let miny = points.iter().map(|x| x.y).min().unwrap();
    let maxx = points.iter().map(|x| x.x).max().unwrap();
    let minx = points.iter().map(|x| x.x).min().unwrap();
    let mut stack = vec![Point { x: 0, y: 0, z: 0 }];
    let mut seen = HashSet::new();
    let k = Point { x: 2, y: 2, z: 5 };
    while !stack.is_empty() {
        let current = stack.pop().unwrap();
        for i in 0..points.len() {
            if ps[i].intersection(&to_points(current)).count() == 4 {
                for p in ps[i].intersection(&to_points(current)) {
                    if *p == k {
                        println!("H {:?}", current)
                    }
                    all_points.insert(*p);
                }
            }
        }
        let Point { x, y, z } = current;
        for (x, y, z) in [
            (x + 1, y, z),
            (x - 1, y, z),
            (x, y + 1, z),
            (x, y - 1, z),
            (x, y, z + 1),
            (x, y, z - 1),
        ] {
            let p = Point { x, y, z };
            if seen.contains(&p) {
                continue;
            }
            seen.insert(p);
            if existing_points.contains(&p) {
                continue;
            }
            if x >= minx - 10
                && x <= maxx + 10
                && y >= miny - 10
                && y <= maxy + 10
                && z >= minz - 10
                && z <= maxz + 10
            {
                stack.push(p)
            }
        }
    }

    println!("{}", existing_points.len());
    println!("{}", all_points.len());
}
