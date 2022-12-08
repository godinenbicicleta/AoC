use std::cell::RefCell;
use std::fs;
use std::rc::{Rc, Weak};
use std::str::FromStr;

#[derive(Debug)]
struct Tree {
    root: Rc<Dir>,
    dirs: Vec<Weak<Dir>>,
}

#[derive(Debug)]
struct Dir {
    name: String,
    parent: RefCell<Weak<Dir>>,
    children: RefCell<Vec<Rc<Dir>>>,
    size: RefCell<u32>,
}

fn build(s: String) -> Tree {
    let root_dir = Rc::new(Dir {
        name: "/".to_string(),
        parent: RefCell::new(Weak::new()),
        children: RefCell::new(vec![]),
        size: RefCell::new(0),
    });
    let dirs = vec![];
    let mut tree = Tree {
        root: Rc::clone(&root_dir),
        dirs,
    };
    let mut current = Rc::clone(&root_dir);
    for line in s.lines().skip(1) {
        if line.starts_with("$ ls") {
            continue;
        }
        if line.starts_with("$ cd ..") {
            let parent = current.parent.borrow().upgrade().unwrap();
            current = Rc::clone(&parent);
            continue;
        }
        if line.starts_with("$ cd") {
            let to_name = line.strip_prefix("$ cd ").unwrap();
            let mut new_current = Rc::clone(&current);
            for child in current.children.borrow().iter() {
                if child.name == to_name {
                    new_current = Rc::clone(child);
                    break;
                }
            }
            current = new_current;
            continue;
        }
        if line.starts_with("dir ") {
            let dir_name = line.strip_prefix("dir ").unwrap();
            let dir = Rc::new(Dir {
                name: dir_name.to_string(),
                parent: RefCell::new(Weak::new()),
                children: RefCell::new(vec![]),
                size: RefCell::new(0),
            });
            *dir.parent.borrow_mut() = Rc::downgrade(&current);
            tree.dirs.push(Rc::downgrade(&dir));
            current.children.borrow_mut().push(Rc::clone(&dir));
            continue;
        }
        // we have a file
        let (size, _) = line.split_once(" ").unwrap();
        let size_num = u32::from_str(size).expect(size);
        let mut parent = Some(Rc::clone(&current));
        while let Some(p) = parent {
            *p.size.borrow_mut() += size_num;
            parent = p.parent.borrow().upgrade();
        }
    }
    tree
}

pub fn run() {
    println!("day07");
    let s = fs::read_to_string("data/day07.txt").unwrap();
    let tree = build(s);
    let p1: u32 = tree
        .dirs
        .iter()
        .map(|x| x.upgrade().unwrap().size.borrow().to_owned())
        .filter(|x| *x <= 100_000)
        .sum();
    println!("PART 1: {}", p1);
    let total_size = tree.root.size.borrow().to_owned();
    let needed = 30000000 - (70000000 - total_size);
    let p2 = tree
        .dirs
        .iter()
        .map(|x| x.upgrade().unwrap().size.borrow().to_owned())
        .filter(|x| *x >= needed)
        .min()
        .unwrap();
    println!("PART 2: {}", p2);
}
