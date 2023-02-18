use std::fs;
use std::str::FromStr;

struct Monkey {
    inspected: u128,
    items: Vec<u128>,
    operation: Box<dyn Fn(u128) -> u128>,
    test_num: u128,
    if_true: usize,
    if_false: usize,
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
    let op: Box<dyn (Fn(u128) -> u128)> = match lines
        .next()
        .unwrap()
        .strip_prefix("  Operation: new = old ")
        .unwrap()
        .split_once(' ')
        .unwrap()
    {
        ("*", n) => {
            let num = u128::from_str(n).ok();
            if let Some(parsed_n) = num {
                Box::new(move |x: u128| x * parsed_n)
            } else {
                Box::new(|x: u128| x * x)
            }
        }

        ("+", n) => {
            let num = u128::from_str(n).ok();
            if let Some(parsed_n) = num {
                Box::new(move |x: u128| x + parsed_n)
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

pub fn run() {
    println!("day11");
    let s = fs::read_to_string("data/day11.txt").unwrap();

    let mut prod = 1;
    for (part, rounds) in [(1, 20), (2, 10000)] {
        let mut monkeys = Vec::new();
        for monkey_data in s.split("\n\n") {
            let monkey = parse(monkey_data);
            prod *= monkey.test_num;
            monkeys.push(monkey);
        }
        let num_monkeys = monkeys.len();
        for _ in 0..rounds {
            for ix in 0..num_monkeys {
                let mut inspected = 0;
                let mut moves = Vec::new();
                for item in &monkeys[ix].items {
                    inspected += 1;
                    let mut wl = (*monkeys[ix].operation)(*item);

                    wl = if part == 1 { wl / 3 } else { wl % prod };
                    let test_num = monkeys[ix].test_num;
                    if wl % test_num == 0 {
                        moves.push((monkeys[ix].if_true, wl))
                    } else {
                        moves.push((monkeys[ix].if_false, wl))
                    }
                }
                monkeys[ix].inspected += inspected;
                monkeys[ix].items = Vec::new();
                for (dest, wl) in moves {
                    monkeys[dest].items.push(wl)
                }
            }
        }
        let mut inspects = monkeys.iter().map(|m| (m.inspected)).collect::<Vec<_>>();
        inspects.sort_by(|a, b| b.cmp(a));
        println!(
            "PART {}: {} ({:?})",
            part,
            inspects[0] * inspects[1],
            inspects
        );
    }
}
