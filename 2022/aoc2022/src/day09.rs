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
                if num.0 == 0 {
                    print!("H");
                } else if num.0 == knots.len() - 1 {
                    print!("T");
                } else {
                    print!("{}", num.0);
                }
            } else if x == 0 && y == 0 {
                print!("S");
            } else {
                print!(".");
            }
        }
        println!();
    }
}

fn move_knot(t: Pos, h: Pos) -> Pos {
    match (h.x-t.x, h.y-t.y) => {
        (0,0) => t,
        (0,2) =>  Pos { x: t.x, y: t.y + 1 },
        (0,-2) =>  Pos { x: t.x, y: t.y - 1 },
        (2,0) =>Pos { y: t.y, x: t.x + 1 },
        (-2,0) =>  Pos { y: t.y, x: t.x - 1 },

    }
    match (h, t) {
        (a, b) if a == b => a,
        (Pos { x: hx, y: hy }, Pos { x: tx, y: ty }) if hx == tx && hy - ty == 2 => {
            Pos { x: tx, y: ty + 1 }
        }
        (Pos { x: hx, y: hy }, Pos { x: tx, y: ty }) if hx == tx && ty - hy == 2 => {
            Pos { x: tx, y: ty - 1 }
        }
        (Pos { x: hx, y: hy }, Pos { x: tx, y: ty }) if hy == ty && hx - tx == 2 => {
            Pos { y: ty, x: t.x + 1 }
        }
        (Pos { x: hx, y: hy }, Pos { x: tx, y: ty }) if hy == ty && tx - hx == 2 => {
            Pos { y: ty, x: t.x - 1 }
        }
        // diagonal 1 step
        (Pos { x: hx, y: hy }, Pos { x: tx, y: ty }) if hx - tx == 1 && hy - ty == 2 => Pos {
            x: tx + 1,
            y: ty + 1,
        },
        (Pos { x: hx, y: hy }, Pos { x: tx, y: ty }) if hx - tx == 1 && ty - hy == 2 => Pos {
            x: tx + 1,
            y: ty - 1,
        },
        (Pos { x: hx, y: hy }, Pos { x: tx, y: ty }) if hx - tx == 2 && hy - ty == 1 => Pos {
            x: tx + 1,
            y: ty + 1,
        },
        (Pos { x: hx, y: hy }, Pos { x: tx, y: ty }) if hx - tx == 2 && ty - hy == 1 => Pos {
            x: tx + 1,
            y: ty - 1,
        },
        (Pos { x: hx, y: hy }, Pos { x: tx, y: ty }) if tx - hx == 2 && ty - hy == 1 => Pos {
            x: tx - 1,
            y: ty - 1,
        },
        (Pos { x: hx, y: hy }, Pos { x: tx, y: ty }) if tx - hx == 2 && hy - ty == 1 => Pos {
            x: tx - 1,
            y: ty + 1,
        },
        (Pos { x: hx, y: hy }, Pos { x: tx, y: ty }) if tx - hx == 1 && ty - hy == 2 => Pos {
            x: tx - 1,
            y: ty - 1,
        },
        (Pos { x: hx, y: hy }, Pos { x: tx, y: ty }) if tx - hx == 1 && hy - ty == 2 => Pos {
            x: tx - 1,
            y: ty + 1,
        },
        // diagonal 2 steps
        (Pos { x: hx, y: hy }, Pos { x: tx, y: ty }) if hx - tx == 2 && hy - ty == 2 => Pos {
            x: tx + 1,
            y: ty + 1,
        },
        (Pos { x: hx, y: hy }, Pos { x: tx, y: ty }) if hx - tx == 2 && ty - hy == 2 => Pos {
            x: tx + 1,
            y: ty - 1,
        },
        (Pos { x: hx, y: hy }, Pos { x: tx, y: ty }) if tx - hx == 2 && hy - ty == 2 => Pos {
            x: tx - 1,
            y: ty + 1,
        },
        (Pos { x: hx, y: hy }, Pos { x: tx, y: ty }) if tx - hx == 2 && ty - hy == 2 => Pos {
            x: tx - 1,
            y: ty - 1,
        },
        _ => t,
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
