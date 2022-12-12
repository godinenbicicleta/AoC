use std::fs;
use std::str::FromStr;

struct Monkey {
    inspected: u128,
    items: Vec<u128>,
    operation: Box<dyn Fn(u128) -> u128>,
    send_to: Box<dyn Fn(u128) -> usize>,
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
        .map(|x| u128::from_str(x).unwrap())
        .collect();
    let op: Box<dyn Fn(u128) -> u128> = match lines
        .next()
        .unwrap()
        .strip_prefix("  Operation: new = old ")
        .unwrap()
        .split_once(" ")
        .unwrap()
    {
        ("*", n) => {
            let num = u128::from_str(n).ok();
            Box::new(move |old: u128| {
                if let Some(n) = num {
                    old * n
                } else {
                    old * old
                }
            })
        }

        ("+", n) => {
            let num = u128::from_str(n).ok();
            Box::new(move |old: u128| {
                if let Some(n) = num {
                    old + n
                } else {
                    old + old
                }
            })
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
        send_to: Box::new(move |x| if x % test_num == 0 { if_true } else { if_false }),
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

pub fn run() {
    println!("day11");
    let s = fs::read_to_string("data/day11_test.txt").unwrap();
    let primes = get_primes();
    println!("{:?}", primes[..10].to_owned());

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
                    let mut wl = (monkeys[ix].operation)(*item) / div;
                    let dest = (monkeys[ix].send_to)(wl);
                    for n in &primes {
                        if *n > wl {
                            break;
                        }
                        if wl % *n == 0 {
                            wl = wl / *n;
                        }
                    }

                    moves.push((dest, wl));
                }
                monkeys[ix].inspected += inspected;
                monkeys[ix].items = Vec::new();
                for (dest, wl) in moves {
                    monkeys[dest].items.push(wl)
                }
            }
            println!(
                "round: {} | {:?} {}",
                round, monkeys[0].items, monkeys[0].inspected
            );
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
