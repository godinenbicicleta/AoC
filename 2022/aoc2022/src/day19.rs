use std::collections::HashMap;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::str::FromStr;

#[derive(Debug)]
struct Blueprint {
    id: u32,
    ore: Resources,
    clay: Resources,
    obsidian: Resources,
    geode: Resources,
}

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
struct Resources {
    ore: u32,
    clay: u32,
    obsidian: u32,
    geode: u32,
}
#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
struct Robots {
    ore: u32,
    clay: u32,
    obsidian: u32,
    geode: u32,
}

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
enum Resource {
    Ore,
    Clay,
    Obsidian,
    Geode,
}

struct Round {
    i: u8,
    resources: Resources,
    robots: Robots,
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

fn parse_robot(s: &str) -> Resources {
    let mut m = HashMap::new();
    if s.contains("and") {
        let parts = s.split_once("costs ").unwrap().1.split(" and ");
        for s in parts {
            let mut parts = s.split_whitespace();
            let num = u32::from_str(parts.next().unwrap()).unwrap();
            m.insert(parse_one(parts.next().unwrap()), num);
        }
    } else {
        let mut parts = s.split_once("costs ").unwrap().1.split_whitespace();
        let num = u32::from_str(parts.next().unwrap()).unwrap();
        m.insert(parse_one(parts.next().unwrap()), num);
    };

    Resources {
        ore: *m.get(&Resource::Ore).unwrap_or(&0),
        clay: *m.get(&Resource::Clay).unwrap_or(&0),
        obsidian: *m.get(&Resource::Obsidian).unwrap_or(&0),
        geode: *m.get(&Resource::Geode).unwrap_or(&0),
    }
}

fn can_buy(resources: Resources, cost: Resources) -> bool {
    resources.ore >= cost.ore
        && resources.obsidian >= cost.obsidian
        && resources.clay >= cost.clay
        && resources.geode >= cost.geode
}

fn minus_cost(resources: Resources, cost: Resources) -> Resources {
    Resources {
        ore: resources.ore - cost.ore,
        clay: resources.clay - cost.clay,
        obsidian: resources.obsidian - cost.obsidian,
        geode: resources.geode - cost.geode,
    }
}
fn add_robot(robots: Robots, robot: Resource) -> Robots {
    match robot {
        Resource::Clay => Robots {
            clay: robots.clay + 1,
            ..robots
        },
        Resource::Ore => Robots {
            ore: robots.ore + 1,
            ..robots
        },
        Resource::Geode => Robots {
            geode: robots.geode + 1,
            ..robots
        },
        Resource::Obsidian => Robots {
            obsidian: robots.obsidian + 1,
            ..robots
        },
    }
}
fn add_resources(left: Resources, right: Robots) -> Resources {
    Resources {
        ore: left.ore + right.ore,
        clay: left.clay + right.clay,
        obsidian: left.obsidian + right.obsidian,
        geode: left.geode + right.geode,
    }
}

fn get_geodes(b: &Blueprint, rounds: u8) -> u32 {
    let mut seen: HashMap<u8, (u32, u32)> = HashMap::new();
    let mut states = vec![Round {
        i: 0,
        resources: Resources {
            ore: 0,
            clay: 0,
            obsidian: 0,
            geode: 0,
        },
        robots: Robots {
            ore: 1,
            clay: 0,
            obsidian: 0,
            geode: 0,
        },
    }];
    let mut max_score: u32 = 0;
    while !states.is_empty() {
        let state = states.pop().unwrap();
        if seen.contains_key(&state.i) {
            let (seen_geode_re, seen_geode_ro) = seen.get(&state.i).unwrap();
            if *seen_geode_re > state.resources.geode && *seen_geode_ro > state.robots.geode {
                continue;
            }
            if state.resources.geode > *seen_geode_re && state.robots.geode > *seen_geode_ro {
                seen.insert(state.i, (state.resources.geode, state.robots.geode));
            }
        } else {
            seen.insert(state.i, (state.resources.geode, state.robots.geode));
        }

        let round_no = state.i + 1;
        if round_no > rounds {
            max_score = max_score.max(state.resources.geode);
            continue;
        }

        let resources = state.resources;
        let robots = state.robots;

        let mut new_resources = vec![resources];
        let mut new_robots = vec![robots];

        if can_buy(resources, b.geode) {
            new_resources = vec![minus_cost(resources, b.geode)];
            new_robots = vec![add_robot(robots, Resource::Geode)];
        } else {
            for (cost, resource) in [b.obsidian, b.clay, b.ore].iter().zip([
                Resource::Obsidian,
                Resource::Clay,
                Resource::Ore,
            ]) {
                if can_buy(resources, *cost) {
                    let cond = match resource {
                        Resource::Obsidian => {
                            robots.obsidian > b.geode.obsidian
                                && robots.obsidian > b.obsidian.obsidian
                                && robots.obsidian > b.clay.obsidian
                                && robots.obsidian > b.ore.obsidian
                        }
                        Resource::Clay => {
                            robots.clay > b.geode.clay
                                && robots.clay > b.obsidian.clay
                                && robots.clay > b.clay.clay
                                && robots.clay > b.ore.clay
                        }
                        Resource::Ore => {
                            robots.ore > b.geode.ore
                                && robots.ore > b.obsidian.ore
                                && robots.ore > b.clay.ore
                                && robots.ore > b.ore.ore
                        }
                        _ => unreachable!(),
                    };
                    if cond {
                        continue;
                    }
                    new_resources.push(minus_cost(resources, *cost));
                    new_robots.push(add_robot(robots, resource));
                }
            }
        }

        let new_resources = new_resources.iter().map(|x| add_resources(*x, robots));

        for (resource, robot) in new_resources.zip(new_robots) {
            states.push(Round {
                i: round_no,
                resources: resource,
                robots: robot,
            });
        }
    }
    max_score
}

pub fn run() {
    println!("day19");
    let f = File::open("data/day19.txt").unwrap();
    let mut blueprints: Vec<Blueprint> = Vec::new();
    let mut id = 1;
    for line in BufReader::new(f).lines() {
        let line = line.unwrap().to_owned();
        let line = line.split_once(": ");
        let mut costs = line.unwrap().1.split(". ");
        let ore = parse_robot(costs.next().unwrap());
        let clay = parse_robot(costs.next().unwrap());
        let obsidian = parse_robot(costs.next().unwrap());
        let geode = parse_robot(costs.next().unwrap());
        let b = Blueprint {
            id,
            ore,
            clay,
            obsidian,
            geode,
        };
        id += 1;
        blueprints.push(b);
    }
    let mut p1 = 0;
    for blueprint in blueprints.iter() {
        let score = get_geodes(blueprint, 24);
        let quality = score * blueprint.id;
        println!("{}: {score} | {quality}", blueprint.id);
        p1 += quality;
    }
    println!("PART 1: {p1}");
    let mut p2 = 1;
    for blueprint in blueprints.iter().take(3) {
        let score = get_geodes(blueprint, 32);
        println!("{}: {score}", blueprint.id);
        p2 *= score;
    }
    println!("PART 2: {p2}");
}
