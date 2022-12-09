use std::fs;

#[derive(Debug, Clone, Copy)]
struct Max {
    top: i32,
    right: i32,
    bottom: i32,
    left: i32,
}

// :execute "vert" "help"
// :execute 'vsplit' | terminal 'cargo' 'run'
pub fn run() {
    println!("day08");
    let mut arr: Vec<Vec<i32>> = Vec::new();
    let s = fs::read_to_string("data/day08.txt").unwrap();
    let mut max_heights: Vec<Vec<Max>> = Vec::new();
    for line in s.lines() {
        let mut v = Vec::new();
        let mut hs = Vec::new();
        for c in line.chars() {
            v.push(c.to_digit(10).unwrap() as i32);
            hs.push(Max {
                top: -1,
                right: -1,
                bottom: -1,
                left: -1,
            });
        }
        arr.push(v);
        max_heights.push(hs);
    }
    let rows = arr.len();
    let cols = arr[0].len();

    // fill max heights
    for y in 0..rows {
        for x in 0..cols {
            let h = arr[y][x];
            if x == 0 {
                max_heights[y][x] = Max {
                    left: h,
                    ..max_heights[y][x]
                }
            } else {
                max_heights[y][x] = Max {
                    left: h.max(max_heights[y][x - 1].left),
                    ..max_heights[y][x]
                }
            }

            if y == 0 {
                max_heights[y][x] = Max {
                    top: h,
                    ..max_heights[y][x]
                }
            } else {
                max_heights[y][x] = Max {
                    top: h.max(max_heights[y - 1][x].top),
                    ..max_heights[y][x]
                }
            }
        }
    }
    for y in (0..rows).rev() {
        for x in (0..cols).rev() {
            let h = arr[y][x];
            if x == cols - 1 {
                max_heights[y][x] = Max {
                    right: h,
                    ..max_heights[y][x]
                }
            } else {
                max_heights[y][x] = Max {
                    right: h.max(max_heights[y][x + 1].right),
                    ..max_heights[y][x]
                }
            }

            if y == rows - 1 {
                max_heights[y][x] = Max {
                    bottom: h,
                    ..max_heights[y][x]
                }
            } else {
                max_heights[y][x] = Max {
                    bottom: h.max(max_heights[y + 1][x].bottom),
                    ..max_heights[y][x]
                }
            }
        }
    }

    let mut visible = 0;
    for y in 0..rows {
        for x in 0..cols {
            if x == 0 || y == 0 || x == cols - 1 || y == rows - 1 {
                visible += 1;
                continue;
            }
            let h = arr[y][x];
            let ns = [
                max_heights[y - 1][x].top,
                max_heights[y + 1][x].bottom,
                max_heights[y][x - 1].left,
                max_heights[y][x + 1].right,
            ];
            for n in ns {
                if n < h {
                    visible += 1;
                    break;
                }
            }
        }
    }
    println!("PART 1: {}", visible);
    let mut score = -1;
    for y in 0..rows {
        for x in 0..cols {
            let mut left = 0;
            let mut right = 0;
            let mut top = 0;
            let mut bottom = 0;
            // visible left
            for i in (0..x).rev() {
                left += 1;
                if arr[y][x] <= arr[y][i] {
                    break;
                }
            }
            // visible right
            for i in (x + 1)..cols {
                right += 1;
                if arr[y][x] <= arr[y][i] {
                    break;
                }
            }
            // visible top
            for j in (0..y).rev() {
                top += 1;
                if arr[y][x] <= arr[j][x] {
                    break;
                }
            }
            // visible bottom
            for j in (y + 1)..rows {
                bottom += 1;
                if arr[y][x] <= arr[j][x] {
                    break;
                }
            }
            score = score.max(left * right * bottom * top);
        }
    }
    println!("PART 2: {}", score);
}
