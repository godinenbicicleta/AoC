use std::fs;
use std::str::FromStr;

pub fn run() {
    println!("day04");
    for (label, file_name) in [(" (test)", "data/day04_test.txt"), ("", "data/day04.txt")] {
        let s = fs::read_to_string(file_name).unwrap();
        let mut p1 = 0;
        let mut p2 = 0;
        for line in s.lines() {
            let mut bounds = line
                .split(",")
                .map(|s| s.split("-").map(|s| i32::from_str(s).unwrap()));

            let mut left = bounds.next().unwrap();
            let left_min = left.next().unwrap();
            let left_max = left.next().unwrap();

            let mut right = bounds.next().unwrap();
            let right_min = right.next().unwrap();
            let right_max = right.next().unwrap();

            let c1 = left_min <= right_min && left_max >= right_max;
            let c2 = right_min <= left_min && right_max >= left_max;
            if c1 || c2 {
                p1 += 1;
            }
            let c1 = left_max < right_min;
            let c2 = right_max < left_min;
            if !(c1 || c2) {
                p2 += 1;
            }
        }
        println!("PART 1{}: {}", label, p1);
        println!("PART 2{}: {}", label, p2);
    }
}
