use std::collections::{HashMap, HashSet};
use std::fs;
use std::str::FromStr;
#[derive(Debug, Clone, Copy, Eq, PartialEq, Hash)]
struct Point {
    x: i32,
    y: i32,
    z: i32,
}

fn to_points(p: Point) -> HashSet<Point> {
    let mut s = HashSet::new();
    for x in [p.x - 1, p.x] {
        for y in [p.y - 1, p.y] {
            for z in [p.z - 1, p.z] {
                s.insert(Point { x, y, z });
            }
        }
    }
    s
}

#[derive(Debug, Eq, Hash, Copy, Clone, PartialEq)]
enum Dir {
    Xp,
    Yp,
    Zp,
    Xn,
    Yn,
    Zn,
}

#[derive(Debug, Clone)]
struct Face {
    points: Vec<Point>,
}

fn to_faces(p: Point) -> HashMap<Dir, Face> {
    let mut zps = Vec::new();
    let mut yps = Vec::new();
    let mut xps = Vec::new();
    for x in [p.x, p.x - 1] {
        for y in [p.y, p.y - 1] {
            zps.push(Point { x, y, z: p.z })
        }
    }
    for x in [p.x, p.x - 1] {
        for z in [p.z, p.z - 1] {
            yps.push(Point { x, y: p.y, z })
        }
    }
    for z in [p.z, p.z - 1] {
        for y in [p.y, p.y - 1] {
            xps.push(Point { x: p.x, y, z })
        }
    }
    let zp = Face { points: zps };
    let yp = Face { points: yps };
    let xp = Face { points: xps };
    let mut zns = Vec::new();
    let mut yns = Vec::new();
    let mut xns = Vec::new();
    for x in [p.x, p.x - 1] {
        for y in [p.y, p.y - 1] {
            zns.push(Point { x, y, z: p.z - 1 })
        }
    }
    for x in [p.x, p.x - 1] {
        for z in [p.z, p.z - 1] {
            yns.push(Point { x, y: p.y - 1, z })
        }
    }
    for z in [p.z, p.z - 1] {
        for y in [p.y, p.y - 1] {
            xns.push(Point { x: p.x - 1, y, z })
        }
    }
    let zn = Face { points: zns };
    let yn = Face { points: yns };
    let xn = Face { points: xns };

    let mut h = HashMap::new();
    h.insert(Dir::Zp, zp);
    h.insert(Dir::Zn, zn);
    h.insert(Dir::Xp, xp);
    h.insert(Dir::Xn, xn);
    h.insert(Dir::Yp, yp);
    h.insert(Dir::Yn, yn);
    h
}

fn dedup(v: Vec<HashSet<Point>>) -> Vec<HashSet<Point>> {
    let mut res = Vec::new();
    'outer: for i in 0..v.len() {
        for j in i + 1..v.len() - 1 {
            if v[i] == v[j] {
                continue 'outer;
            }
        }
        res.push(v[i].clone());
    }
    res
}
pub fn run() {
    println!("day18");

    let s = fs::read_to_string("data/day18.txt").unwrap();
    let mut points = Vec::new();
    for line in s.lines() {
        let mut coords = line.split(',').map(|x| i32::from_str(x).unwrap());
        let x = coords.next().unwrap();
        let y = coords.next().unwrap();
        let z = coords.next().unwrap();
        points.push(Point { x, y, z })
    }
    let mut part1 = points.len() * 6;
    let ps: Vec<_> = points.iter().map(|x| to_points(*x)).collect();
    for i in 0..points.len() - 1 {
        for j in i..points.len() {
            if ps[i].intersection(&ps[j]).count() == 4 {
                part1 -= 2;
            }
        }
    }
    let all_points: HashSet<_> = points.iter().copied().collect();
    println!("PART 1: {part1}");
    let faces: Vec<HashMap<Dir, Face>> = points.iter().map(|x| to_faces(*x)).collect();
    let mut faces_all = Vec::new();
    for face_dict in faces.iter() {
        for face in face_dict.values() {
            let ps: HashSet<Point> = face.points.iter().copied().collect();
            faces_all.push(ps);
        }
    }
    faces_all = dedup(faces_all);
    let maxz = points.iter().map(|x| x.z).max().unwrap() + 2;
    let minz = points.iter().map(|x| x.z).min().unwrap() - 2;
    let maxy = points.iter().map(|x| x.y).max().unwrap() + 2;
    let miny = points.iter().map(|x| x.y).min().unwrap() - 2;
    let maxx = points.iter().map(|x| x.x).max().unwrap() + 2;
    let minx = points.iter().map(|x| x.x).min().unwrap() - 2;
    println!("{}", faces_all.len());

    let start = Point {
        x: minx,
        y: miny,
        z: minz,
    };
    let mut stack = vec![start];
    let mut seen = HashSet::new();
    let mut area = 0;
    seen.insert(start);
    while !stack.is_empty() {
        let point = stack.pop().unwrap();
        let mut to_remove = Vec::new();
        for f in faces_all.iter() {
            for face in to_faces(point).values() {
                let hs: HashSet<_> = face.points.iter().copied().collect();
                if hs == *f {
                    area += 1;
                    to_remove.push(f.clone());
                }
            }
        }
        faces_all.retain(|x| to_remove.iter().all(|y| *y != *x));
        for p in [
            Point {
                x: point.x + 1,
                ..point
            },
            Point {
                y: point.y + 1,
                ..point
            },
            Point {
                z: point.z + 1,
                ..point
            },
            Point {
                x: point.x - 1,
                ..point
            },
            Point {
                y: point.y - 1,
                ..point
            },
            Point {
                z: point.z - 1,
                ..point
            },
        ] {
            if p.x > maxx || p.x < minx || p.y > maxy || p.y < miny || p.z > maxz || p.z < minz {
                continue;
            }
            if seen.contains(&p) {
                continue;
            }
            if all_points.contains(&p) {
                continue;
            }
            seen.insert(p);
            stack.push(p);
        }
    }
    println!("PART 2: {area}");
}
// 3266 not answer
