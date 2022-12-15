use std::collections::HashMap;
use std::fs;
use std::str::FromStr;

fn parse_comma(s: &str) -> (u32, u32) {
    let (left, right) = s.split_once(",").unwrap();
    (u32::from_str(left).unwrap(), u32::from_str(right).unwrap())
}

fn parse(start: &str, end: &str) -> Vec<(u32, u32)> {
    let (startx, starty) = parse_comma(start);
    let (endx, endy) = parse_comma(end);
    let mut v = Vec::new();
    let sx = startx.min(endx);
    let sy = starty.min(endy);
    let ex = startx.max(endx);
    let ey = starty.max(endy);
    for x in sx..=ex {
        for y in sy..=ey {
            v.push((x, y))
        }
    }
    v
}

#[allow(dead_code)]
fn display(m: &HashMap<(u32, u32), char>, maxy: u32, minx: u32, maxx: u32) {
    for y in 0..=maxy {
        for x in minx..=maxx {
            match m.get(&(x, y)) {
                Some(c) => print!("{}", c),
                _ => print!("."),
            }
        }
        println!();
    }
}

fn get_move(p: (u32, u32), map: &HashMap<(u32, u32), char>) -> Option<(u32, u32)> {
    // down
    if map.get(&(p.0, p.1 + 1)).is_none() {
        return Some((p.0, p.1 + 1));
    }
    // down left
    if map.get(&(p.0 - 1, p.1 + 1)).is_none() {
        return Some((p.0 - 1, p.1 + 1));
    }
    // own right
    if map.get(&(p.0 + 1, p.1 + 1)).is_none() {
        return Some((p.0 + 1, p.1 + 1));
    }
    return None;
}
fn get_move2(p: (u32, u32), map: &HashMap<(u32, u32), char>, maxy: u32) -> Option<(u32, u32)> {
    // down
    if map.get(&(p.0, p.1 + 1)).is_none() && p.1 + 1 < maxy + 2 {
        return Some((p.0, p.1 + 1));
    }
    // down left
    if map.get(&(p.0 - 1, p.1 + 1)).is_none() && p.1 + 1 < maxy + 2 {
        return Some((p.0 - 1, p.1 + 1));
    }
    // own right
    if map.get(&(p.0 + 1, p.1 + 1)).is_none() && p.1 + 1 < maxy + 2 {
        return Some((p.0 + 1, p.1 + 1));
    }
    return None;
}

fn parse_map(s: &str) -> (HashMap<(u32, u32), char>, u32, u32, u32) {
    let mut map = HashMap::new();
    let mut maxy = 0;
    let mut minx = 0;
    let mut maxx = 0;
    for line in s.lines() {
        for (segment_start, segment_end) in line.split(" -> ").zip(line.split(" -> ").skip(1)) {
            for coords in parse(segment_start, segment_end).into_iter() {
                map.insert(coords, '#');
                if coords.1 > maxy {
                    maxy = coords.1;
                }
                if coords.0 > maxx {
                    maxx = coords.0;
                }
                if (minx == 0 && coords.0 > 0) || (coords.0 < minx) {
                    minx = coords.0;
                }
            }
        }
    }
    (map, minx, maxx, maxy)
}

#[allow(unreachable_code, unused_variables)]
pub fn run() {
    println!("day14");
    let s = fs::read_to_string("data/day14.txt").unwrap();
    let (mut map, minx, maxx, maxy) = parse_map(&s);
    let mut p1 = 0;
    let start = (500, 0);
    'outer: loop {
        let mut pos = start;
        loop {
            match get_move(pos, &mut map) {
                None => {
                    map.insert(pos, 'o');
                    p1 += 1;
                    break;
                }
                Some((x, y)) => pos = (x, y),
            }
            if pos.1 > maxy {
                break 'outer;
            }
        }
    }
    //    display(&map, maxy, minx, maxx);
    println!("PART 1: {}", p1);
    let (mut map, minx, maxx, maxy) = parse_map(&s);
    let mut p2 = 0;
    let start = (500, 0);
    'outer: loop {
        let mut pos = start;
        loop {
            match get_move2(pos, &mut map, maxy) {
                None => {
                    map.insert(pos, 'o');
                    p2 += 1;
                    if pos == start {
                        break 'outer;
                    }
                    break;
                }
                Some((x, y)) => pos = (x, y),
            }
        }
    }
    println!("PART 2: {}", p2);
    //display(&map, maxy, minx, maxx);
}
