use std::collections::{HashMap, HashSet, VecDeque};
use std::fs;

enum Direction {
    N,
    S,
    W,
    E,
}

fn print_grid(g: &HashSet<(i32, i32)>) {
    let minx = g.iter().map(|x| x.0).min().unwrap();
    let maxx = g.iter().map(|x| x.0).max().unwrap();
    let miny = g.iter().map(|x| x.1).min().unwrap();
    let maxy = g.iter().map(|x| x.1).max().unwrap();
    println!();
    println!("{}", (maxx - minx + 1) * (maxy - miny + 1) - g.len() as i32);
}
pub fn run() {
    println!("day23");

    let s = fs::read_to_string("data/day23.txt").unwrap();
    let mut g = HashSet::new();
    for (y, line) in s.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c == '#' {
                g.insert((x as i32, y as i32));
            }
        }
    }
    let mut directions =
        VecDeque::from_iter([Direction::N, Direction::S, Direction::W, Direction::E]);
    for round in 0.. {
        //println!("round {round}");
        //print_grid(&g);
        let mut moving = Vec::new();
        let mut not_moving = Vec::new();
        let elfs = g.clone();
        'outer2: for elf in elfs.iter() {
            for position in [
                (elf.0 + 1, elf.1),
                (elf.0 + 1, elf.1 + 1),
                (elf.0 + 1, elf.1 - 1),
                (elf.0, elf.1 + 1),
                (elf.0, elf.1 - 1),
                (elf.0 - 1, elf.1 - 1),
                (elf.0 - 1, elf.1 + 1),
                (elf.0 - 1, elf.1),
            ] {
                if g.contains(&position) {
                    moving.push(elf);
                    continue 'outer2;
                }
            }
            not_moving.push(elf);
        }
        if moving.is_empty() {
            println!("EMPTY");
            println!("{}", round + 1);
            break;
        }

        let mut propositions = HashMap::new();

        for elf in moving {
            let mut proposed = false;
            'outer: for direction in directions.iter() {
                match *direction {
                    Direction::N => {
                        for position in [
                            (elf.0 - 1, elf.1 - 1),
                            (elf.0, elf.1 - 1),
                            (elf.0 + 1, elf.1 - 1),
                        ] {
                            if g.contains(&position) {
                                continue 'outer;
                            }
                        }
                        propositions
                            .entry((elf.0, elf.1 - 1))
                            .or_insert(Vec::new())
                            .push(elf);
                        proposed = true;
                        break;
                    }
                    Direction::S => {
                        for position in [
                            (elf.0 - 1, elf.1 + 1),
                            (elf.0, elf.1 + 1),
                            (elf.0 + 1, elf.1 + 1),
                        ] {
                            if g.contains(&position) {
                                continue 'outer;
                            }
                        }
                        propositions
                            .entry((elf.0, elf.1 + 1))
                            .or_insert(Vec::new())
                            .push(elf);
                        proposed = true;
                        break;
                    }
                    Direction::E => {
                        for position in [
                            (elf.0 + 1, elf.1),
                            (elf.0 + 1, elf.1 + 1),
                            (elf.0 + 1, elf.1 - 1),
                        ] {
                            if g.contains(&position) {
                                continue 'outer;
                            }
                        }
                        propositions
                            .entry((elf.0 + 1, elf.1))
                            .or_insert(Vec::new())
                            .push(elf);
                        proposed = true;
                        break;
                    }
                    Direction::W => {
                        for position in [
                            (elf.0 - 1, elf.1 + 1),
                            (elf.0 - 1, elf.1 - 1),
                            (elf.0 - 1, elf.1),
                        ] {
                            if g.contains(&position) {
                                continue 'outer;
                            }
                        }
                        propositions
                            .entry((elf.0 - 1, elf.1))
                            .or_insert(Vec::new())
                            .push(elf);
                        proposed = true;
                        break;
                    }
                }
            }
            if !proposed {
                not_moving.push(elf);
            }
        }
        g.clear();
        for (new_pos, elf_vec) in propositions {
            if elf_vec.len() == 1 {
                g.insert(new_pos);
            } else {
                for pos in elf_vec.iter() {
                    g.insert(**pos);
                }
            }
        }
        for pos in not_moving {
            g.insert(*pos);
        }
        let f = directions.pop_front().unwrap();
        directions.push_back(f);
    }
    print_grid(&g);
}
