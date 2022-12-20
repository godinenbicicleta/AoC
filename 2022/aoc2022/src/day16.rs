use std::collections::{HashMap, HashSet, VecDeque};
use std::fs;
use std::str::FromStr;

#[derive(Clone, Debug)]
struct Valve {
    flow: i32,
    to: Vec<String>,
}

fn path_to(goal: &str, d: HashMap<String, String>) -> Vec<String> {
    let mut path = vec![goal.to_owned()];
    let mut current = goal.to_string();
    while d.get(&current).is_some() {
        current = d.get(&current).unwrap().to_owned();
        path.push(current.to_owned());
    }
    path.into_iter().rev().skip(1).collect::<Vec<String>>()
}
fn shortest_path(start: &str, goal: &str, valves: &HashMap<String, Valve>) -> Vec<String> {
    let mut seen = HashSet::new();
    let mut prev: HashMap<String, String> = HashMap::new();
    let mut queue = VecDeque::new();
    seen.insert(start.to_owned());
    queue.push_back(start.to_owned());
    while !queue.is_empty() {
        let current = queue.pop_front().unwrap();
        if current == goal {
            let p = path_to(goal, prev);
            return p;
        }
        for dest in valves.get(&current).unwrap().to.iter() {
            if seen.contains(dest) {
                continue;
            }
            seen.insert(dest.to_string());
            prev.insert(dest.to_owned(), current.to_owned());
            queue.push_back((*dest).to_string());
        }
    }
    unreachable!();
}

fn get_score2(
    current: (String, String),
    valves: &HashMap<String, Valve>,
    visited: Vec<(String, String)>,
    time_remaining: (i32, i32),
    short_cache: &mut HashMap<(String, String), usize>,
    cache: &mut HashMap<String, i32>,
) -> i32 {
    let visited_tot = visited
        .iter()
        .flat_map(|(x, y)| [x.to_owned(), y.to_owned()])
        .collect::<Vec<String>>();
    let mut unvisited: Vec<String> = valves
        .keys()
        .filter(|x| !visited_tot.contains(x) && valves.get(&x.to_string()).unwrap().flow > 0)
        .map(|x| x.to_string())
        .collect();
    unvisited.sort();
    let key1 = vec![
        unvisited.join(","),
        format!("({}, {})", current.0, current.1).to_string(),
        format!("<{} {}>", time_remaining.0, time_remaining.1).to_string(),
    ]
    .join("|");
    let key2 = vec![
        unvisited.join(","),
        format!("({}, {})", current.1, current.0).to_string(),
        format!("<{} {}>", time_remaining.1, time_remaining.0).to_string(),
    ]
    .join("|");

    if cache.get(&key1).is_some() {
        return *cache.get(&key1).unwrap();
    }
    if cache.get(&key2).is_some() {
        return *cache.get(&key2).unwrap();
    }
    let mut max_score = 0;
    for valve1 in unvisited.iter() {
        if *valve1 == current.0 {
            continue;
        }
        for valve2 in unvisited.iter() {
            if valve1 == valve2 || *valve2 == current.1 {
                continue;
            }
            let short1 = match short_cache.get(&(current.0.to_string(), (*valve1).to_string())) {
                Some(v) => *v,
                None => {
                    let v = shortest_path(&current.0, valve1, &valves);
                    short_cache.insert((current.0.to_owned(), (*valve1).to_owned()), v.len());
                    v.len()
                }
            };
            let short2 = match short_cache.get(&(current.1.to_string(), (*valve2).to_string())) {
                Some(v) => *v,
                None => {
                    let v = shortest_path(&current.1, valve2, &valves);
                    short_cache.insert((current.1.to_owned(), (*valve2).to_owned()), v.len());
                    v.len()
                }
            };
            let mut time_remaining1 = time_remaining.0 - short1 as i32 - 1;
            let mut time_remaining2 = time_remaining.1 - short2 as i32 - 1;
            if time_remaining1 < 0 && time_remaining2 < 0 {
                continue;
            }
            time_remaining1 = time_remaining1.max(0);
            time_remaining2 = time_remaining2.max(0);

            let (v1, score_delta1) = if time_remaining1 <= 0 {
                (current.0.to_string(), 0)
            } else {
                (
                    valve1.to_string(),
                    time_remaining1 * valves.get(valve1).unwrap().flow,
                )
            };
            let (v2, score_delta2) = if time_remaining2 <= 0 {
                (current.1.to_string(), 0)
            } else {
                (
                    valve2.to_string(),
                    time_remaining2 * valves.get(valve2).unwrap().flow,
                )
            };
            let score = score_delta1
                + score_delta2
                + get_score2(
                    (v1.to_string(), v2.to_string()),
                    valves,
                    visited
                        .iter()
                        .map(|x| (x.0.to_string(), x.1.to_string()))
                        .chain(
                            [(v1.to_string(), v2.to_string())]
                                .iter()
                                .map(|x| (x.0.to_string(), x.1.to_string())),
                        )
                        .collect(),
                    (time_remaining1, time_remaining2),
                    short_cache,
                    cache,
                );
            max_score = max_score.max(score);
        }
    }

    cache.insert(key1, max_score);
    cache.insert(key2, max_score);
    max_score
}

fn get_score(
    current: String,
    valves: &HashMap<String, Valve>,
    visited: Vec<String>,
    time_remaining: i32,
    short_cache: &mut HashMap<(String, String), usize>,
    cache: &mut HashMap<String, i32>,
) -> i32 {
    let mut unvisited: Vec<String> = valves
        .keys()
        .filter(|x| !visited.contains(x))
        .map(|x| x.to_string())
        .collect();
    unvisited.sort();
    let key = vec![
        unvisited.join(","),
        format!("({})", current).to_string(),
        format!("<{}>", time_remaining).to_string(),
    ]
    .join("|");

    if cache.get(&key).is_some() {
        return *cache.get(&key).unwrap();
    }

    let mut max_score = 0;
    for valve in valves.keys() {
        if visited.contains(valve) || *valve == current || valves.get(valve).unwrap().flow == 0 {
            continue;
        }
        let short = match short_cache.get(&(current.to_string(), (*valve).to_string())) {
            Some(v) => *v,
            None => {
                let v = shortest_path(&current, valve, &valves);
                short_cache.insert((current.to_owned(), (*valve).to_owned()), v.len());
                v.len()
            }
        };
        let time_remaining = time_remaining - short as i32 - 1;
        if time_remaining <= 0 {
            continue;
        }
        let mut score = time_remaining * valves.get(valve).unwrap().flow;
        score = score
            + get_score(
                valve.to_string(),
                valves,
                visited
                    .iter()
                    .map(|x| x.to_string())
                    .chain([valve.to_string()].iter().map(|x| x.to_string()))
                    .collect(),
                time_remaining,
                short_cache,
                cache,
            );
        max_score = max_score.max(score);
    }
    cache.insert(key, max_score);
    max_score
}

pub fn run() {
    println!("day16");
    let s = fs::read_to_string("data/day16_test.txt").unwrap();
    let mut valves: HashMap<String, Valve> = HashMap::new();
    for line in s.lines() {
        let (left, right) = if line.contains("tunnels") {
            line.split_once("; tunnels lead to valves ").unwrap()
        } else {
            line.split_once("; tunnel leads to valve ").unwrap()
        };
        let id = left
            .strip_prefix("Valve ")
            .and_then(|x| x.split_whitespace().next())
            .unwrap();
        let (_, flow_str) = left.split_once("rate=").unwrap();
        let flow = i32::from_str(flow_str).unwrap();
        let vs = right.split(", ").map(|x| x.to_string()).collect();
        valves.insert(id.to_string(), Valve { flow, to: vs });
    }
    let mut short_cache: HashMap<(String, String), usize> = HashMap::new();
    let mut cache = HashMap::new();
    let s = get_score(
        "AA".to_string(),
        &valves,
        Vec::new(),
        30,
        &mut short_cache,
        &mut cache,
    );
    println!("PART 1: {}", s);
    let mut cache = HashMap::new();
    let s = get_score2(
        ("AA".to_string(), "AA".to_string()),
        &valves,
        Vec::new(),
        (26, 26),
        &mut short_cache,
        &mut cache,
    );
    println!("PART 2: {}", s);
}
