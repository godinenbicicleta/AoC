use std::collections::HashSet;
use std::fs;
use std::str::FromStr;

#[derive(Hash, Eq, PartialEq, Copy, Clone, Debug)]
struct Pos {
    x: i32,
    y: i32,
}
#[allow(dead_code)]
fn print_grid(knots: &[Pos]) {
    for y in (-20..20).rev() {
        for x in -20..20 {
            if let Some(num) = knots.iter().enumerate().find(|(_, p)| **p == Pos { x, y }) {
                match num.0 {
                    0 => print!("H"),
                    n if n == knots.len() - 1 => print!("T"),
                    _ => print!("{}", num.0),
                }
                continue;
            }
            if x == 0 && y == 0 {
                print!("S");
                continue;
            }
            print!(".");
        }
        println!();
    }
}

fn move_knot(t: Pos, h: Pos) -> Pos {
    let (dx, dy) = match (h.x - t.x, h.y - t.y) {
        (0, 2) => (0, 1),
        (0, -2) => (0, -1),
        (2, 0) => (1, 0),
        (-2, 0) => (-1, 0),
        (2, 2) | (1, 2) | (2, 1) => (1, 1),
        (2, -1) | (1, -2) | (2, -2) => (1, -1),
        (-2, 1) | (-1, 2) | (-2, 2) => (-1, 1),
        (-1, -2) | (-2, -2) | (-2, -1) => (-1, -1),
        _ => (0, 0),
    };
    Pos {
        x: t.x + dx,
        y: t.y + dy,
    }
}

pub fn run() {
    println!("day09");
    let s = fs::read_to_string("data/day09.txt").unwrap();
    for (label, num_knots) in [("PART 1", 2), ("PART 2", 10)] {
        let mut knots = Vec::new();
        for _ in 0..num_knots {
            knots.push(Pos { x: 0, y: 0 });
        }
        let mut seen = HashSet::new();
        seen.insert(*knots.last().unwrap());
        for line in s.lines() {
            let mut parts = line.split_whitespace();
            let dir = parts.next().unwrap();
            let s_num = parts.next().unwrap();
            let num = i32::from_str(s_num).unwrap();
            for _ in 0..num {
                let mut h = knots[0];
                h = match dir {
                    "U" => Pos { x: h.x, y: h.y + 1 },
                    "D" => Pos { x: h.x, y: h.y - 1 },
                    "L" => Pos { x: h.x - 1, y: h.y },
                    "R" => Pos { x: h.x + 1, y: h.y },
                    _ => unreachable!(),
                };
                knots[0] = h;
                for i in 1..knots.len() {
                    knots[i] = move_knot(knots[i], knots[i - 1]);
                }
                seen.insert(*knots.last().unwrap());
            }
        }
        println!("{}: {}", label, seen.len());
    }
}
