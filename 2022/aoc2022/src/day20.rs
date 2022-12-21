use std::fs;
use std::str::FromStr;

pub fn run() {
    println!("day20");
    for (key, times) in [(1, 1), (811589153, 10)] {
        let s = fs::read_to_string("data/day20.txt").unwrap();
        let mut nums = s
            .lines()
            .map(|x| i128::from_str(x).unwrap() * key)
            .enumerate()
            .collect::<Vec<(usize, i128)>>();
        let reference: Vec<(usize, i128)> = nums.clone();
        for _ in 0..times {
            for (ix, target) in reference.iter() {
                if *target == 0 {
                    continue;
                }
                let j = nums
                    .iter()
                    .enumerate()
                    .find(|(_, (i, x))| *x == *target && i == ix)
                    .unwrap()
                    .0;
                let num = nums.remove(j);
                let s = nums.len();
                if num.1 + j as i128 > 0 {
                    nums.insert((num.1 + j as i128) as usize % s, num);
                } else if j as i128 + num.1 == 0 {
                    nums.push(num);
                } else {
                    let pos = s - ((j as i128 + num.1).abs() as usize % s);
                    nums.insert(pos, num);
                }
            }
        }
        let index = nums
            .iter()
            .enumerate()
            .find(|(_, (_, x))| *x == 0)
            .unwrap()
            .0;
        let a = nums[(index + 1000) % reference.len()];
        let b = nums[(index + 2000) % reference.len()];
        let c = nums[(index + 3000) % reference.len()];

        println!("{} {} {} ({})", a.1, b.1, c.1, a.1 + b.1 + c.1);
    }
}
