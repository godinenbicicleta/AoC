use std::cell::RefCell;
use std::fs;
use std::rc::{Rc, Weak};
use std::str::FromStr;

#[derive(Debug)]
struct Tree {
    root: Rc<Node>,
    dirs: Vec<Weak<Node>>,
}

#[derive(Debug)]
struct Node {
    name: String,
    parent: RefCell<Weak<Node>>,
    children: RefCell<Vec<Rc<Node>>>,
    size: RefCell<u32>,
}

fn build(s: String) -> Tree {
    let root = Rc::new(Node {
        name: "/".to_string(),
        parent: RefCell::new(Weak::new()),
        children: RefCell::new(vec![]),
        size: RefCell::new(0),
    });
    let dirs = vec![];
    let mut tree = Tree { root, dirs };
    let mut current = Rc::clone(&tree.root);
    'outer: for line in s.lines().skip(1) {
        if line.starts_with("$ ls") {
            continue;
        }
        if line.starts_with("$ cd ..") {
            let parent = current.parent.borrow().upgrade().unwrap();
            current = parent;
            continue;
        }
        if line.starts_with("$ cd") {
            let to_name = line.strip_prefix("$ cd ").unwrap();
            let children = current.children.borrow().to_owned();
            for child in children.iter() {
                if child.name == to_name {
                    current = Rc::clone(&Rc::clone(child));
                    continue 'outer;
                }
            }
        }
        if line.starts_with("dir ") {
            let dir_name = line.strip_prefix("dir ").unwrap();
            let node = Rc::new(Node {
                name: dir_name.to_string(),
                parent: RefCell::new(Weak::new()),
                children: RefCell::new(vec![]),
                size: RefCell::new(0),
            });
            *node.parent.borrow_mut() = Rc::downgrade(&current);
            current.children.borrow_mut().push(Rc::clone(&node));
            tree.dirs.push(Rc::downgrade(&node));
            continue;
        }
        // we have a file
        let (size, name) = line.split_once(" ").unwrap();
        let size_num = u32::from_str(size).expect(size);
        let node = Rc::new(Node {
            name: name.to_string(),
            parent: RefCell::new(Weak::new()),
            children: RefCell::new(vec![]),
            size: RefCell::new(size_num),
        });
        *node.parent.borrow_mut() = Rc::downgrade(&current);
        let mut n = node;
        loop {
            if let Some(p) = n.parent.borrow().upgrade() {
                *p.size.borrow_mut() += size_num;
            } else {
                break;
            }
            let k = n.parent.borrow().upgrade().unwrap();
            n = Rc::clone(&k);
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
    let total_size = Rc::clone(&tree.root).size.borrow().to_owned();
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
