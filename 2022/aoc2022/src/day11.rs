use std::collections::HashMap;
use std::fs;
use std::str::FromStr;

struct Monkey {
    inspected: u128,
    items: Vec<Item>,
    operation: Operation,
    test_num: u128,
    if_true: usize,
    if_false: usize,
}
#[derive(Debug, Clone)]
struct Item {
    id: usize,
    wl: Box<Num>,
}

enum Operation {
    Square,
    Sum(u128),
    Mult(u128),
}

#[derive(Debug, Clone, Eq, Hash, PartialEq)]
enum Num {
    N(u128),
    Add(Vec<Num>),
    Prod(Vec<Num>),
}

fn parse(s: &str) -> Monkey {
    let mut lines = s.lines();
    lines.next();
    let items_line = lines.next().unwrap();
    let items: Vec<_> = items_line
        .split_once("Starting items: ")
        .unwrap()
        .1
        .split(", ")
        .map(|x| Item {
            id: usize::from_str(x).unwrap(),
            wl: Box::new(Num::N(u128::from_str(x).unwrap())),
        })
        .collect();
    let op: Operation = match lines
        .next()
        .unwrap()
        .strip_prefix("  Operation: new = old ")
        .unwrap()
        .split_once(" ")
        .unwrap()
    {
        ("*", n) => {
            let num = u128::from_str(n).ok();
            if let Some(n) = num {
                Operation::Mult(n)
            } else {
                Operation::Square
            }
        }

        ("+", n) => {
            let num = u128::from_str(n).ok();
            if let Some(n) = num {
                Operation::Sum(n)
            } else {
                unreachable!()
            }
        }
        _ => unreachable!(),
    };
    let test_num: u128 = lines
        .next()
        .unwrap()
        .strip_prefix("  Test: divisible by ")
        .map(|x| u128::from_str(x).unwrap())
        .unwrap();
    let if_true: usize = lines
        .next()
        .unwrap()
        .strip_prefix("    If true: throw to monkey ")
        .map(|x| usize::from_str(x).unwrap())
        .unwrap();
    let if_false: usize = lines
        .next()
        .unwrap()
        .strip_prefix("    If false: throw to monkey ")
        .map(|x| usize::from_str(x).unwrap())
        .unwrap();

    Monkey {
        inspected: 0,
        items,
        operation: op,
        test_num,
        if_true,
        if_false,
    }
}

fn get_primes() -> Vec<u128> {
    let mut sieve = vec![true; 1000002];
    sieve[0] = false;
    sieve[1] = false;
    for i in 2..1000002 {
        if sieve[i] {
            let mut n = i * i;
            while n < 1000002 {
                sieve[n] = false;
                n += i;
            }
        }
    }
    let mut p = Vec::new();
    for (ix, elem) in sieve.iter().enumerate() {
        if *elem && ix > 100 {
            p.push(ix as u128)
        }
    }
    p
}

fn reduce(n: Box<Num>) -> u128 {
    match *n {
        Num::N(n) => n,
        Num::Add(x, y) => reduce(x) + reduce(y),
        Num::Prod(x, y) => reduce(x) * reduce(y),
    }
}

fn to_string(n: &Box<Num>) -> String {
    let mut s = String::new();
    match n.as_ref() {
        Num::N(x) => s.push_str(&format!("{}", x)),
        Num::Add(x, y) => {
            let x = to_string(x);
            let y = to_string(y);
            s.push_str(&format!("({}+{})", x, y))
        }
        Num::Prod(x, y) => {
            let x = to_string(x);
            let y = to_string(y);
            s.push_str(&format!("({}*{})", x, y))
        }
    };
    s
}

fn divide(n: Box<Num>, div: u128) -> Num {
    let n = reduce(n);
    Num::N(n / div)
}

fn rem(wl: Box<Num>, t: u128, cache: &mut HashMap<(String, u128), u128>) -> u128 {
    //let s = to_string(&wl);
    //let res = cache.get(&(s.to_string(), t));
    //if res.is_some() {
    //    return *res.unwrap();
    //}
    let res = match *wl {
        Num::N(n) => n % t,
        Num::Add(x, y) => (rem(x, t, cache) + rem(y, t, cache)) % t,
        Num::Prod(x, y) => {
            let p1 = rem(x, t, cache);
            if p1 == 0 {
                0
            } else {
                let p2 = rem(y, t, cache);
                if p2 == 0 {
                    0
                } else {
                    (p1 * p2) % t
                }
            }
        }
    };
    //cache.insert((s, t), res);
    res
}

fn run_test(wl: Box<Num>, t: u128, cache: &mut HashMap<(String, u128), u128>) -> bool {
    rem(wl, t, cache) == 0
}

pub fn run() {
    println!("day11");
    let s = fs::read_to_string("data/day11_test.txt").unwrap();
    let primes = get_primes();
    println!("{:?}", primes[..10].to_owned());
    let mut cache = HashMap::new();

    for (part, div, rounds) in [(1, 3, 20), (2, 1, 10000)] {
        let mut monkeys = Vec::new();
        for monkey_data in s.split("\n\n") {
            let monkey = parse(monkey_data);
            monkeys.push(monkey);
        }
        for monkey in &monkeys {
            println!("Monkey {:?}", monkey.items);
        }
        let num_monkeys = monkeys.len();
        for round in 0..rounds {
            for ix in 0..num_monkeys {
                let mut inspected = 0;
                let mut moves = Vec::new();
                for item in &monkeys[ix].items {
                    inspected += 1;
                    let mut wl = match monkeys[ix].operation {
                        Operation::Sum(n) => {
                            Box::new(Num::Add(item.wl.clone(), Box::new(Num::N(n))))
                        }
                        Operation::Square => Box::new(Num::Prod(item.wl.clone(), item.wl.clone())),
                        Operation::Mult(n) => {
                            Box::new(Num::Prod(item.wl.clone(), Box::new(Num::N(n))))
                        }
                    };
                    if div != 1 {
                        wl = Box::new(divide(wl, div));
                    }
                    let test_num = monkeys[ix].test_num;
                    if run_test(wl.clone(), test_num, &mut cache) {
                        moves.push((monkeys[ix].if_true, Item { id: item.id, wl }))
                    } else {
                        moves.push((monkeys[ix].if_false, Item { id: item.id, wl }))
                    }
                }
                monkeys[ix].inspected += inspected;
                monkeys[ix].items = Vec::new();
                for (dest, wl) in moves {
                    monkeys[dest].items.push(wl)
                }
            }
            if round % 200 == 0 || round == 19 {
                println!(
                    "round: {} | {} {:?}",
                    round, monkeys[0].inspected, monkeys[3].inspected,
                );
            }
        }
        let mut inspects = monkeys.iter().map(|m| (m.inspected)).collect::<Vec<_>>();
        inspects.sort_by(|a, b| b.cmp(&a));
        println!(
            "PART {}: {} ({:?})",
            part,
            inspects[0] * inspects[1],
            inspects
        );
    }
}
