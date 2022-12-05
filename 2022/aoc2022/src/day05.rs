use std::collections::HashMap;
use std::fs;
use std::str::FromStr;

type Stacks = HashMap<u32, Vec<char>>;

fn parse(conf: &str) -> Stacks {
    let mut stacks = HashMap::new();
    let mut index_to_stack: HashMap<usize, u32> = HashMap::new();
    let ids_line = conf.lines().last().unwrap();
    for (index, c) in ids_line.chars().enumerate() {
        if let Some(stack) = c.to_digit(10) {
            index_to_stack.insert(index, stack);
            stacks.insert(stack, Vec::new());
        }
    }
    for line in conf.lines() {
        if line.contains("1") {
            break;
        }
        for (index, c) in line.chars().enumerate().filter(|(_, c)| c.is_alphabetic()) {
            if let Some(stack) = index_to_stack.get(&index) {
                stacks.get_mut(stack).unwrap().push(c);
            }
        }
    }

    for (_, value) in &mut stacks {
        value.reverse();
    }
    stacks
}

pub fn run() {
    println!("day05");
    for (label, file_name) in [(" (test)", "data/day05_test.txt"), ("", "data/day05.txt")] {
        let s = fs::read_to_string(file_name).unwrap();
        let (conf, ins) = s.split_once("\n\n").unwrap();
        for part in [1, 2] {
            let mut stacks = parse(conf);

            for instruction in ins.lines() {
                match instruction.split_whitespace().collect::<Vec<_>>()[..] {
                    ["move", amount, "from", from, "to", to] => {
                        let amount = usize::from_str(amount).unwrap();
                        let from = u32::from_str(from).unwrap();
                        let to = u32::from_str(to).unwrap();
                        let mut popped_elems = Vec::new();
                        for _ in 0..amount {
                            let popped = stacks.get_mut(&from).unwrap().pop().unwrap();
                            popped_elems.push(popped);
                        }
                        if part == 2 {
                            popped_elems.reverse();
                        }
                        stacks.get_mut(&to).unwrap().extend(popped_elems);
                    }
                    _ => unreachable!(),
                }
            }
            let mut sorted_keys: Vec<_> = stacks.keys().collect();
            sorted_keys.sort();
            let mut res = String::new();
            for key in sorted_keys {
                res.push(*stacks.get(key).unwrap().last().unwrap());
            }
            println!("PART {}{}: {}", part, label, res);
        }
    }
}
