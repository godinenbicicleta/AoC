use std::collections::{HashMap, HashSet};
use std::fs;
use std::str::FromStr;

fn dist(x: (i32, i32), y: (i32, i32)) -> i32 {
    (x.0 - y.0).abs() + (x.1 - y.1).abs()
}
pub fn run() {
    println!("day15");
    let s = fs::read_to_string("data/day15.txt").unwrap();
    let mut map = HashMap::new();
    let mut sensor_to_closest = HashMap::new();
    for line in s.lines() {
        let (sensor_part, beacon_part) = line.split_once(": closest beacon is at ").unwrap();
        let (sx_part, sy_part) = sensor_part.split_once(", ").unwrap();
        let sx = i32::from_str(sx_part.strip_prefix("Sensor at x=").unwrap()).unwrap();
        let sy = i32::from_str(sy_part.strip_prefix("y=").unwrap()).unwrap();
        let (bx_part, by_part) = beacon_part.split_once(", ").unwrap();
        let bx = i32::from_str(bx_part.strip_prefix("x=").unwrap()).unwrap();
        let by = i32::from_str(by_part.strip_prefix("y=").unwrap()).unwrap();
        map.insert((sx, sy), 'S');
        map.insert((bx, by), 'B');
        sensor_to_closest.insert((sx, sy), dist((sx, sy), (bx, by)));
    }
    let target_row = 2000000;
    let mut blocked = HashSet::new();
    for ((sx, sy), d) in sensor_to_closest.iter() {
        let mut min_dist = (target_row - sy).abs();
        let mut i = 0;
        while min_dist <= *d {
            if map.get(&(sx + i, target_row)).is_none() {
                blocked.insert((sx + i, target_row));
            }
            if map.get(&(sx - i, target_row)).is_none() {
                blocked.insert((sx - i, target_row));
            }
            i += 1;
            min_dist = dist((sx - i, target_row), (*sx, *sy));
        }
    }
    println!("PART 1: {}", blocked.len());
    let n = 4000000;

    'f: for distance_inc in 1.. {
        for (cs, d) in sensor_to_closest.iter() {
            let distance = d + distance_inc;
            let mut candidates = Vec::new();
            for dx in 0..=distance {
                let x = cs.0 + dx;
                candidates.push((x, cs.1 + distance - dx));
                candidates.push((x, -(cs.1 + distance - dx)));
            }
            for dx in -distance..0 {
                let x = cs.0 + dx;
                candidates.push((x, cs.1 + dx + distance));
                candidates.push((x, -(cs.1 + dx + distance)));
            }
            'outer: while !candidates.is_empty() {
                let candidate = candidates.pop().unwrap();
                if candidate.0 < 0
                    || candidate.0 > n as i32
                    || candidate.1 > n as i32
                    || candidate.1 < 0
                {
                    continue;
                }
                if map.get(&candidate).is_some() {
                    continue;
                }
                for (&sensor, &d) in sensor_to_closest.iter() {
                    if dist(candidate, sensor) <= d {
                        continue 'outer;
                    }
                }
                println!(
                    "PART 2: {}",
                    candidate.0 as u128 * 4000000 + candidate.1 as u128
                );
                break 'f;
            }
        }
    }
}
