use std::fs;
use std::str::FromStr;
fn print_crt(crt: &mut i32, x: i32) {
    if (x - 1..x + 2).contains(crt) {
        print! {"{}", '\u{2588}'}
    } else {
        print! {"{}", " "}
    }
    *crt += 1;
    if *crt == 40 {
        println!();
        *crt = *crt % 40;
    }
}
pub fn run() {
    println!("day10");
    let s = fs::read_to_string("data/day10.txt").unwrap();
    let mut cycles = Vec::with_capacity(220);
    let mut x = 1;
    let mut crt = 0;
    cycles.push(x);
    for line in s.lines() {
        let mut parts = line.split_whitespace();
        let instruction = parts.next().unwrap();
        match instruction {
            "noop" => {
                print_crt(&mut crt, x);
                cycles.push(x);
            }
            "addx" => {
                let num = i32::from_str(parts.next().unwrap()).unwrap();
                for _ in 0..2 {
                    cycles.push(x);
                    print_crt(&mut crt, x);
                }
                x += num;
            }
            _ => unreachable!(),
        }
    }
    println!();
    let mut p1 = 0;
    for i in [20, 60, 100, 140, 180, 220] {
        p1 += cycles[i] * i as i32;
    }
    println!("PART 1: {}", p1);
}
