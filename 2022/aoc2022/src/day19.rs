use std::collections::{HashMap, VecDeque};
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::str::FromStr;

#[derive(Debug)]
struct Blueprint {
    id: u32,
    ore: HashMap<Resource, u32>,
    clay: HashMap<Resource, u32>,
    obsidian: HashMap<Resource, u32>,
    geode: HashMap<Resource, u32>,
}

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
enum Resource {
    Ore,
    Clay,
    Obsidian,
    Geode,
}

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
struct Robots {
    ore: u32,
    clay: u32,
    obsidian: u32,
    geode: u32,
}

fn parse_one(s: &str) -> Resource {
    match s {
        "ore" => Resource::Ore,
        "clay" => Resource::Clay,
        "obsidian" => Resource::Obsidian,
        "geode" => Resource::Geode,
        "ore." => Resource::Ore,
        "clay." => Resource::Clay,
        "obsidian." => Resource::Obsidian,
        "geode." => Resource::Geode,
        _ => unreachable!(),
    }
}

fn parse_robot(s: &str) -> HashMap<Resource, u32> {
    let mut m = HashMap::new();
    if s.contains("and") {
        let parts = s.split_once("costs ").unwrap().1.split(" and ");
        for s in parts {
            println!("{s}");
            let mut parts = s.split_whitespace();
            let num = u32::from_str(parts.next().unwrap()).unwrap();
            m.insert(parse_one(parts.next().unwrap()), num);
        }
    } else {
        let mut parts = s.split_once("costs ").unwrap().1.split_whitespace();
        let num = u32::from_str(parts.next().unwrap()).unwrap();
        m.insert(parse_one(parts.next().unwrap()), num);
    };

    m
}

fn get_options(
    resources: Robots,
    b: &Blueprint,
    cache: &mut HashMap<(Robots, u32), Vec<Vec<Resource>>>,
) -> Vec<Vec<Resource>> {
    if cache.contains_key(&(resources, b.id)) {
        return (*cache.get(&(resources, b.id)).unwrap()).clone();
    }
    let mut res = Vec::new();
    let mut ore = true;
    let mut ore_resources = resources.to_owned();
    for (key, value) in b.ore.iter() {
        match key {
            Resource::Ore => {
                if resources.ore < *value {
                    ore = false;
                    break;
                }
                ore_resources.ore -= value;
            }
            Resource::Clay => {
                if resources.clay < *value {
                    ore = false;
                    break;
                }
                ore_resources.clay -= value;
            }
            Resource::Obsidian => {
                if resources.obsidian < *value {
                    ore = false;
                    break;
                }
                ore_resources.obsidian -= value;
            }
            Resource::Geode => {
                if resources.geode < *value {
                    ore = false;
                    break;
                }
                ore_resources.geode -= value;
            }
        }
    }
    if ore {
        res.push(vec![Resource::Ore]);
        for mut elem in get_options(ore_resources, b, cache) {
            elem.push(Resource::Ore);
            res.push(elem);
        }
    }

    let mut clay = true;
    let mut clay_resources = resources.to_owned();
    for (key, value) in b.ore.iter() {
        match key {
            Resource::Ore => {
                if resources.ore < *value {
                    clay = false;
                    break;
                }
                clay_resources.ore -= value;
            }
            Resource::Clay => {
                if resources.clay < *value {
                    clay = false;
                    break;
                }
                clay_resources.clay -= value;
            }
            Resource::Obsidian => {
                if resources.obsidian < *value {
                    clay = false;
                    break;
                }
                clay_resources.obsidian -= value;
            }
            Resource::Geode => {
                if resources.geode < *value {
                    clay = false;
                    break;
                }
                clay_resources.geode -= value;
            }
        }
    }
    if clay {
        res.push(vec![Resource::Clay]);
        for mut elem in get_options(clay_resources, b, cache) {
            elem.push(Resource::Clay);
            res.push(elem);
        }
    }

    let mut obsidian = true;
    let mut obsidian_resources = resources.to_owned();
    for (_, value) in b.obsidian.iter() {
        if resources.obsidian > *value {
            obsidian = false;
            break;
        }
        obsidian_resources.obsidian -= value;
    }
    if obsidian {
        res.push(vec![Resource::Obsidian]);
        for mut elem in get_options(obsidian_resources, b, cache) {
            elem.push(Resource::Obsidian);
            res.push(elem);
        }
    }

    let mut geode = true;
    let mut geode_resources = resources.to_owned();
    for (_, value) in b.geode.iter() {
        if resources.geode > *value {
            geode = false;
            break;
        }
        geode_resources.geode -= value;
    }
    if geode {
        res.push(vec![Resource::Geode]);
        for mut elem in get_options(geode_resources, b, cache) {
            elem.push(Resource::Geode);
            res.push(elem);
        }
    }

    cache.insert((resources, b.id), res.to_owned());
    //println!("Original Resources: {resources:?}");
    //println!("Result: {res:?}");

    res
}

fn find_best(b: &Blueprint) -> u32 {
    let mut seen: HashMap<Robots, u32> = HashMap::new();
    let robs = Robots {
        ore: 1,
        clay: 0,
        obsidian: 0,
        geode: 0,
    };
    let mut states: VecDeque<(u32, Robots, HashMap<Resource, u32>)> = VecDeque::new();
    states.push_front((0, robs, HashMap::new()));
    let mut max_score: u32 = 0;
    seen.insert(robs, 0);
    while !states.is_empty() {
        let (time, robots, resources) = states.pop_front().unwrap();
        if time >= 19 {
            let score: u32 = *resources.get(&Resource::Geode).unwrap_or(&0);
            if score > max_score {
                println!("robots: {robots:?}");
                println!("resources: {resources:?}");
                println!("score: {score}");
                println!("time: {time}");
            }
            max_score = max_score.max(score);
            continue;
        }
        let time = time + 1;
        let mut resources = resources.to_owned();
        *resources.entry(Resource::Ore).or_insert(0) += robots.ore;
        *resources.entry(Resource::Clay).or_insert(0) += robots.clay;
        *resources.entry(Resource::Geode).or_insert(0) += robots.geode;
        *resources.entry(Resource::Obsidian).or_insert(0) += robots.obsidian;
        states.push_back((time, robots, resources.clone()));
        let resources_for_key = Robots {
            ore: *resources.get(&Resource::Ore).unwrap(),
            obsidian: *resources.get(&Resource::Obsidian).unwrap(),
            clay: *resources.get(&Resource::Clay).unwrap(),
            geode: *resources.get(&Resource::Geode).unwrap(),
        };
        let mut cache = HashMap::new();
        for new_robots in get_options(resources_for_key, b, &mut cache).iter() {
            let mut robots = robots;
            let mut new_resources = resources.to_owned();
            for new_robot in new_robots.iter() {
                match new_robot {
                    Resource::Ore => {
                        for (key, value) in b.ore.iter() {
                            new_resources.entry(*key).and_modify(|e| *e -= value);
                        }
                        robots.ore += 1;
                    }
                    Resource::Obsidian => {
                        for (key, value) in b.obsidian.iter() {
                            new_resources.entry(*key).and_modify(|e| *e -= value);
                        }
                        robots.obsidian += 1;
                    }
                    Resource::Geode => {
                        robots.geode += 1;
                        for (key, value) in b.geode.iter() {
                            new_resources.entry(*key).and_modify(|e| *e -= value);
                        }
                    }
                    Resource::Clay => {
                        robots.clay += 1;
                        for (key, value) in b.clay.iter() {
                            new_resources.entry(*key).and_modify(|e| *e -= value);
                        }
                    }
                }
            }
            if !seen.contains_key(&robots) || *seen.get(&robots).unwrap() > time {
                states.push_back((time, robots, new_resources));
                seen.insert(robots, time);
                println!("{robots:?}, {time}");
            }
        }
    }
    max_score
}

pub fn run() {
    println!("day19");
    let f = File::open("data/day19_test.txt").unwrap();
    let mut blueprints: Vec<Blueprint> = Vec::new();
    let mut id = 1;
    for line in BufReader::new(f).lines() {
        let line = line.unwrap().to_owned();
        let line = line.split_once(": ");
        let mut robots = line.unwrap().1.split(". ");
        let ore_robot = parse_robot(robots.next().unwrap());
        let clay_robot = parse_robot(robots.next().unwrap());
        let obsidian_robot = parse_robot(robots.next().unwrap());
        let geode_robot = parse_robot(robots.next().unwrap());
        let b = Blueprint {
            id,
            ore: ore_robot,
            clay: clay_robot,
            obsidian: obsidian_robot,
            geode: geode_robot,
        };
        id += 1;
        blueprints.push(b);
    }
    println!("{blueprints:?}");
    for blueprint in blueprints.iter() {
        let quality = find_best(blueprint);
        println!("{quality}");
        break;
    }
}
