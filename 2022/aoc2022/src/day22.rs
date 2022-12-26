use std::collections::HashMap;
use std::fs;
use std::str::from_utf8;
use std::str::FromStr;

fn to_str(g: &HashMap<(i32, i32), char>) -> String {
    let mut s = String::new();
    let maxy = g.keys().map(|(_, y)| *y).max().unwrap();
    for y in 0..=maxy {
        let maxx = g
            .keys()
            .filter(|(_, y_)| *y_ == y)
            .map(|(x, _)| *x)
            .max()
            .unwrap();
        for x in 0..=maxx {
            s.push(*g.get(&(x, y)).unwrap_or(&' '));
        }
        s.push('\n');
    }
    s
}

fn pos_to_face(pos: (i32, i32), length: i32) -> u8 {
    // small grid
    match pos {
        (x, _y) if x < length => 2,
        (x, _y) if x >= length && x < length * 2 => 3,
        (_x, y) if y < length => 1,
        (x, y) if x >= 2 * length && x < 3 * length && y >= length && y < length * 2 => 4,
        (x, y) if x >= 2 * length && y >= 2 * length && x < 3 * length => 5,
        (x, _y) if x >= 3 * length => 6,
        _ => unreachable!(),
    }
}

#[allow(clippy::collapsible_else_if)]
fn run2(grid: &HashMap<(i32, i32), char>, pos: (i32, i32), instructions: &[u8]) {
    let mut pos = pos;
    let grid = grid.clone();
    let gmaxx = grid.keys().map(|(x, _)| *x).max().unwrap();
    let length = if gmaxx < 20 { 4 } else { 50 };
    let mut dir = 'R';
    let mut i = 0;
    let mut repr = grid.clone();
    println!("{pos:?}");
    repr.insert(pos, '>');
    while i < instructions.len() {
        println!("{pos:?} {dir}");
        println!("{}", to_str(&repr));
        if instructions[i] == b'R' || instructions[i] == b'L' {
            dir = match (instructions[i], dir) {
                (b'R', 'R') => 'D',
                (b'L', 'R') => 'U',
                (b'R', 'D') => 'L',
                (b'L', 'D') => 'R',
                (b'R', 'L') => 'U',
                (b'L', 'L') => 'D',
                (b'R', 'U') => 'R',
                (b'L', 'U') => 'L',
                _ => unreachable!(),
            };

            match dir {
                'U' => repr.insert(pos, '^'),
                'D' => repr.insert(pos, 'v'),
                'R' => repr.insert(pos, '>'),
                'L' => repr.insert(pos, '<'),
                _ => unreachable!(),
            };
            i += 1;
            //println!("DIR {dir}");
            continue;
        }
        let mut num_s = Vec::new();
        num_s.push(instructions[i]);
        loop {
            i += 1;
            if i == instructions.len() {
                break;
            }
            if instructions[i] == b'R' || instructions[i] == b'L' {
                break;
            }
            num_s.push(instructions[i]);
            continue;
        }

        let steps_str = from_utf8(&num_s[..]).unwrap();
        let steps = i32::from_str(steps_str).unwrap();
        //println!("STEPS {steps}");

        for _ in 0..steps {
            let (dx, dy): (i32, i32) = match dir {
                'R' => (1, 0),
                'D' => (0, 1),
                'U' => (0, -1),
                'L' => (-1, 0),
                _ => unreachable!(),
            };
            //println!("{pos:?}");
            match dir {
                'U' => repr.insert(pos, '^'),
                'D' => repr.insert(pos, 'v'),
                'R' => repr.insert(pos, '>'),
                'L' => repr.insert(pos, '<'),
                _ => unreachable!(),
            };
            let new_pos = (pos.0 + dx, pos.1 + dy);
            if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '.' {
                pos = new_pos;
                continue;
            }
            if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '#' {
                break;
            }
            if dy == 0 {
                if dx > 0 {
                    if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '.' {
                        pos = new_pos;
                        continue;
                    } else {
                        //else if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '#' {
                        // we can be in 1,4,6
                        let (new_pos, new_dir) = match pos_to_face(pos, length) {
                            1 => ((4 * length - 1, pos.1 - 2 * length), 'L'), // 6 and to the left
                            4 => ((4 * length - 1 - (pos.1 - length), 2 * length), 'D'),
                            6 => ((3 * length - 1, pos.1 - 2 * length), 'L'),
                            _ => unreachable!(),
                        };
                        if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '.' {
                            pos = new_pos;
                            dir = new_dir;
                            continue;
                        } else {
                            break;
                        }
                    }
                } else {
                    if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '.' {
                        pos = new_pos;
                        continue;
                    } else {
                        // go left from 1,2,5
                        let (new_pos, new_dir) = match pos_to_face(pos, length) {
                            1 => ((1, length - 1), 'D'),                               // 3 and Down
                            2 => ((pos.1 - length, 3 * length - 1), 'U'),              // 6 Up
                            5 => ((pos.1 - 2 * length + length, 2 * length - 1), 'L'), // 3 L
                            _ => unreachable!(),
                        };
                        if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '.' {
                            dir = new_dir;
                            pos = new_pos;
                            continue;
                        } else {
                            break;
                        }
                    }
                }
            } else {
                if dy > 0 {
                    if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '.' {
                        pos = new_pos;
                        continue;
                    } else {
                        //else if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '#' {
                        let (new_pos, new_dir) = match pos_to_face(pos, length) {
                            //
                            2 => ((pos.0 + 2 * length, 3 * length - 1), 'U'), // 5 Up
                            3 => ((2 * length - 1, pos.0 - length + 2 * length), 'R'), // 5 R
                            5 => ((length - 1 - (pos.0 - 2 * length), 2 * length - 1), 'U'), // 2 Up
                            6 => ((0, pos.0 - 3 * length), 'R'),              // 2 R
                            _ => unreachable!(),
                            //
                        };
                        if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '.' {
                            dir = new_dir;
                            pos = new_pos;
                            continue;
                        } else {
                            break;
                        }
                    }
                } else {
                    if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '.' {
                        pos = new_pos;
                        continue;
                    } else {
                        let (new_pos, new_dir) = match pos_to_face(pos, length) {
                            1 => ((pos.0 - 2 * length, length), 'D'), // 2 Down
                            2 => ((pos.0 + 2 * length, 0), 'D'),      // 1 Down
                            3 => ((2 * length, pos.0 - length), 'R'), // 1 Right
                            6 => ((3 * length - 1, pos.0 - 3 * length + length), 'L'), // 4 Left
                            _ => unreachable!(),
                        };
                        //else if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '#' {
                        if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '.' {
                            pos = new_pos;
                            dir = new_dir;
                            continue;
                        } else {
                            break;
                        }
                    }
                }
            }
        }
    }

    println!("{pos:?} {dir}");
    println!("{}", to_str(&repr));
    let mut p2 = (pos.1 + 1) * 1000;
    p2 += 4 * (pos.0 + 1);
    p2 += match dir {
        'U' => 3,
        'R' => 0,
        'L' => 2,
        'D' => 1,
        _ => unreachable!(),
    };
    println!("{p2}");
}

#[allow(clippy::collapsible_else_if)]
fn run1(grid: &HashMap<(i32, i32), char>, pos: (i32, i32), instructions: &[u8]) {
    let mut pos = pos;
    let grid = grid.clone();
    let mut dir = 'R';
    let mut i = 0;
    let mut repr = grid.clone();
    println!("{pos:?}");
    repr.insert(pos, '>');
    while i < instructions.len() {
        //println!("{pos:?} {dir}");
        //println!("{}", to_str(&repr));
        if instructions[i] == b'R' || instructions[i] == b'L' {
            dir = match (instructions[i], dir) {
                (b'R', 'R') => 'D',
                (b'L', 'R') => 'U',
                (b'R', 'D') => 'L',
                (b'L', 'D') => 'R',
                (b'R', 'L') => 'U',
                (b'L', 'L') => 'D',
                (b'R', 'U') => 'R',
                (b'L', 'U') => 'L',
                _ => unreachable!(),
            };
            match dir {
                'U' => repr.insert(pos, '^'),
                'D' => repr.insert(pos, 'v'),
                'R' => repr.insert(pos, '>'),
                'L' => repr.insert(pos, '<'),
                _ => unreachable!(),
            };
            i += 1;
            //println!("DIR {dir}");
            continue;
        }
        let mut num_s = Vec::new();
        num_s.push(instructions[i]);
        loop {
            i += 1;
            if i == instructions.len() {
                break;
            }
            if instructions[i] == b'R' || instructions[i] == b'L' {
                break;
            }
            num_s.push(instructions[i]);
            continue;
        }

        let steps_str = from_utf8(&num_s[..]).unwrap();
        let steps = i32::from_str(steps_str).unwrap();
        //println!("STEPS {steps}");

        let (dx, dy): (i32, i32) = match dir {
            'R' => (1, 0),
            'D' => (0, 1),
            'U' => (0, -1),
            'L' => (-1, 0),
            _ => unreachable!(),
        };

        for _ in 0..steps {
            //println!("{pos:?}");
            match dir {
                'U' => repr.insert(pos, '^'),
                'D' => repr.insert(pos, 'v'),
                'R' => repr.insert(pos, '>'),
                'L' => repr.insert(pos, '<'),
                _ => unreachable!(),
            };
            let new_pos = (pos.0 + dx, pos.1 + dy);
            if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '.' {
                pos = new_pos;
                continue;
            }
            if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '#' {
                break;
            }
            if dy == 0 {
                let minx = grid
                    .iter()
                    .filter(|((_, y), v)| *y == pos.1 && **v != ' ')
                    .map(|(x, _)| x.0)
                    .min()
                    .unwrap();
                let maxx = grid
                    .iter()
                    .filter(|((_, y), v)| *y == pos.1 && **v != ' ')
                    .map(|(x, _)| x.0)
                    .max()
                    .unwrap();
                if dx > 0 {
                    if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '.' {
                        pos = new_pos;
                        continue;
                    } else {
                        //else if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '#' {
                        let new_pos = (minx, pos.1);
                        if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '.' {
                            pos = new_pos;
                            continue;
                        } else {
                            break;
                        }
                    }
                } else {
                    if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '.' {
                        pos = new_pos;
                        continue;
                    } else {
                        //else if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '#' {
                        let new_pos = (maxx, pos.1);
                        if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '.' {
                            pos = new_pos;
                            continue;
                        } else {
                            break;
                        }
                    }
                }
            } else {
                let miny = grid
                    .iter()
                    .filter(|((x, _), _)| *x == pos.0)
                    .map(|(x, _)| x.1)
                    .min()
                    .unwrap();
                let maxy = grid
                    .iter()
                    .filter(|((x, _), _)| *x == pos.0)
                    .map(|(x, _)| x.1)
                    .max()
                    .unwrap();
                if dy > 0 {
                    if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '.' {
                        pos = new_pos;
                        continue;
                    } else {
                        //else if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '#' {
                        let new_pos = (pos.0, miny);
                        if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '.' {
                            pos = new_pos;
                            continue;
                        } else {
                            break;
                        }
                    }
                } else {
                    let new_pos = (pos.0, maxy);
                    if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '.' {
                        pos = new_pos;
                        continue;
                    } else {
                        //else if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '#' {
                        let new_pos = (pos.0, maxy);
                        if grid.get(&new_pos).is_some() && *grid.get(&new_pos).unwrap() == '.' {
                            pos = new_pos;
                            continue;
                        } else {
                            break;
                        }
                    }
                }
            }
        }
    }

    println!("{pos:?} {dir}");
    println!("{}", to_str(&repr));
    let mut p1 = (pos.1 + 1) * 1000;
    p1 += 4 * (pos.0 + 1);
    p1 += match dir {
        'U' => 3,
        'R' => 0,
        'L' => 2,
        'D' => 1,
        _ => unreachable!(),
    };
    println!("{p1}");
}

pub fn run() {
    println!("day22");

    let s = fs::read_to_string("data/day22.txt").unwrap();
    let (grid_str, instructions) = s.split_once("\n\n").unwrap();
    let mut grid = HashMap::new();
    let mut pos = (0, 0);

    for (y, line) in grid_str.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c != ' ' {
                grid.insert((x as i32, y as i32), c);
                if y == 0 && c == '.' && pos == (0, 0) {
                    pos = (x as i32, y as i32);
                }
            }
        }
    }
    let instructions = instructions.trim().as_bytes();
    run1(&grid, pos, instructions);
    run2(&grid, pos, instructions);
}
