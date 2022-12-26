use std::collections::{HashMap, VecDeque};
use std::fs;

fn grid_at(
    t: i32,
    grids: &mut Vec<HashMap<(i32, i32), Vec<char>>>,
    minx: i32,
    maxx: i32,
    miny: i32,
    maxy: i32,
) -> &HashMap<(i32, i32), Vec<char>> {
    if grids.get(t as usize).is_some() {
        return &grids[t as usize];
    }
    if t > (maxy - miny - 1) * (maxx - minx - 1) {
        let new_t = t % ((maxy - miny - 1) * (maxx - minx - 1));
        return grid_at(new_t, grids, minx, maxx, miny, maxy);
    }
    let mut n: HashMap<(i32, i32), Vec<char>> = HashMap::new();
    let prev = grid_at(t - 1, grids, minx, maxx, miny, maxy);
    for (coord, keys) in prev {
        let (x, y) = coord;
        for k in keys.iter() {
            let (mut newx, mut newy) = coord;
            match k {
                '>' => {
                    newx = x + 1;
                    if newx == maxx {
                        newx = minx + 1;
                    }
                }
                '<' => {
                    newx = x - 1;
                    if newx == minx {
                        newx = maxx - 1;
                    }
                }
                '^' => {
                    newy = y - 1;
                    if newy == miny {
                        newy = maxy - 1;
                    }
                }
                'v' => {
                    newy = y + 1;
                    if newy == maxy {
                        newy = miny + 1;
                    }
                }
                _ => unreachable!(),
            };
            n.entry((newx, newy)).or_insert(vec![]).push(*k);
        }
    }
    grids.push(n);
    &grids[t as usize]
}
#[allow(clippy::map_entry)]
#[allow(clippy::too_many_arguments)]
fn solve(
    start: (i32, i32),
    goal: (i32, i32),
    t: i32,
    grids: &mut Vec<HashMap<(i32, i32), Vec<char>>>,
    minx: i32,
    maxx: i32,
    miny: i32,
    maxy: i32,
) -> i32 {
    let mut seen = HashMap::new();
    seen.insert(start, vec![t]);
    let mut queue = VecDeque::new();
    queue.push_back((start, t));
    while !queue.is_empty() {
        let (current, t) = queue.pop_front().unwrap();
        if current == goal {
            return t;
        }
        let grid = grid_at(t + 1, grids, minx, maxx, miny, maxy);
        let (x, y) = current;
        let candidates = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x, y)];
        'outer: for candidate in candidates {
            if grid.contains_key(&candidate) {
                continue;
            }
            if candidate.0 == maxx || candidate.0 == minx {
                continue;
            }
            if candidate.1 == miny && candidate != start && candidate != goal {
                continue;
            }
            if candidate.1 >= maxy && candidate != goal && candidate != start {
                continue;
            }
            if seen.contains_key(&candidate) {
                let seen_ts = seen.get(&candidate).unwrap();
                if seen_ts.contains(&(t + 1)) {
                    continue;
                }
                for seen_t in seen_ts {
                    if *seen_t > t + 1
                        && (seen_t - t - 1) % ((maxy - miny - 1) * (maxx - minx - 1)) == 0
                    {
                        continue 'outer;
                    }
                }
            } else {
                seen.insert(candidate, Vec::new());
            }

            queue.push_back((candidate, t + 1));
            seen.get_mut(&candidate).unwrap().push(t + 1);
        }
    }
    unreachable!()
}

pub fn run() {
    println!("day24");
    let s = fs::read_to_string("data/day24.txt").unwrap();
    let mut g = HashMap::new();
    let mut maxy = 0;
    let mut maxx = 0;
    for (y, line) in s.lines().enumerate() {
        maxy = y;
        for (x, c) in line.chars().enumerate() {
            maxx = x;
            if ['>', '<', '^', 'v'].contains(&c) {
                g.insert((x as i32, y as i32), vec![c]);
            }
        }
    }
    let minx = 0;
    let miny = 0;
    let maxx = maxx as i32;
    let maxy = maxy as i32;
    let goal = (maxx - 1, maxy);
    let start = (1, 0);
    let mut grids = vec![g.clone()];
    let t0 = solve(start, goal, 0, &mut grids, minx, maxx, miny, maxy);
    let t1 = solve(goal, start, t0, &mut grids, minx, maxx, miny, maxy);
    let t2 = solve(start, goal, t1, &mut grids, minx, maxx, miny, maxy);
    println!("{t0} {t2}");
}
