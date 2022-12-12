use std::collections::VecDeque;
use std::fs;
pub fn run() {
    println!("day12");
    let s = fs::read_to_string("data/day12.txt").unwrap();
    let mut grid = Vec::new();
    let mut start1 = (0, 0);
    let mut goal = (0, 0);
    for (y, line) in s.lines().enumerate() {
        let mut v = Vec::new();
        for (x, c) in line.chars().enumerate() {
            match c {
                'S' => {
                    v.push('a');
                    start1 = (x as i32, y as i32);
                }
                'E' => {
                    v.push('z');
                    goal = (x as i32, y as i32);
                }
                x => v.push(x),
            }
        }
        grid.push(v);
    }

    let mut starts = Vec::new();
    for (j, row) in (&grid).iter().enumerate() {
        for (i, col) in (&row).iter().enumerate() {
            if *col == 'a' {
                starts.push((i as i32, j as i32));
            }
        }
    }
    let mut min_steps = -1;
    for start in starts {
        let mut queue = VecDeque::from([(start, 0)]);
        let mut seen = vec![vec![false; grid[0].len()]; grid.len()];
        seen[start.1 as usize][start.0 as usize] = true;
        while !queue.is_empty() {
            let (current, steps) = queue.pop_front().unwrap();
            if steps > min_steps && min_steps > 0 {
                break;
            }
            if current == goal {
                if start == start1 {
                    println!("Part 1: {}", steps);
                }
                if steps < min_steps || min_steps == -1 {
                    min_steps = steps;
                }
                break;
            }
            let (x0, y0) = current;
            for (x, y) in [(x0 + 1, y0), (x0 - 1, y0), (x0, y0 + 1), (x0, y0 - 1)] {
                if x >= 0
                    && x < grid[0].len() as i32
                    && y >= 0
                    && y < grid.len() as i32
                    && (grid[y as usize][x as usize] as i32 - grid[y0 as usize][x0 as usize] as i32)
                        <= 1
                    && !seen[y as usize][x as usize]
                {
                    queue.push_back(((x, y), steps + 1));
                    seen[y as usize][x as usize] = true;
                }
            }
        }
    }
    println!("PART 2: {}", min_steps);
}
