const fs = require("fs");

paths = fs
  .readFileSync(process.argv[2], "utf-8")
  .trim()
  .split("\n")
  .map((x) => x.trim().split(","));

class Position {
  constructor(x, y, steps) {
    this.x = x;
    this.y = y;
    this.steps = steps;
  }

  get key() {
    return `${this.x},${this.y}`;
  }

  get distance() {
    return Math.abs(this.x) + Math.abs(this.y);
  }
}

function pathMap(path) {
  const m = new Map();
  for (let position of path) {
    const existing = m.get(position.key);
    if (existing === undefined) {
      m.set(position.key, position);
    } else if (existing.steps < position.step) {
      null;
    } else {
      m.set(position.key, position);
    }
  }
  return m;
}

function pathIntersection(p, q) {
  return [...p.entries()]
    .filter(([x, y]) => q.has(x))
    .reduce((acc, elem) => {
      acc.set(
        elem[0],
        new Position(elem[1].x, elem[1].y, elem[1].steps + q.get(elem[0]).steps)
      );
      return acc;
    }, new Map());
}

intersection = paths //["R8,U5,L5,D3".split(","), "U7,R6,D4,L4".split(",")]
  .map((path) =>
    path.reduce((acc, elem) => reduce(acc, elem), [new Position(0, 0, 0)])
  )
  .map((path) => {
    return pathMap(path);
  })
  .reduce((acc, elem) => pathIntersection(acc, elem));

function reduce(positionArray, movement) {
  direction = movement[0];
  steps = +movement.slice(1);
  const pos = positionArray[positionArray.length - 1];
  const x = pos.x;
  const y = pos.y;
  const totalSteps = pos.steps;
  for (let s = 1; s <= steps; s++) {
    switch (direction) {
      case "U":
        positionArray.push(new Position(x, y + s, totalSteps + s));
        break;
      case "D":
        positionArray.push(new Position(x, y - s, totalSteps + s));
        break;
      case "L":
        positionArray.push(new Position(x - s, y, totalSteps + s));
        break;
      case "R":
        positionArray.push(new Position(x + s, y, totalSteps + s));
        break;
      default:
        throw new Error(`invalid direction ${direction}`);
    }
  }
  return positionArray;
}

console.log([...intersection].slice(0, 2));
console.log(
  [...intersection]
    .sort((a, b) => a[1].distance - b[1].distance)
    .map(([x, y]) => [y, y.distance])
    .slice(0, 5)
);

console.log(
  [...intersection]
    .sort((a, b) => a[1].steps - b[1].steps)
    .map(([x, y]) => [y, y.distance])
    .slice(0, 5)
);
