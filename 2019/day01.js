const fs = require("fs");

fileName = process.argv[2];

function fuel_for(mass) {
  return Math.max(Math.floor(mass / 3) - 2, 0);
}

function req_fuel(mass) {
  if (mass == 0) {
    return 0;
  } else {
    const fuel = fuel_for(mass);
    return fuel + req_fuel(fuel);
  }
}

data = fs
  .readFileSync(fileName, "utf-8")
  .trim()
  .split("\n")
  .reduce((acc, elem) => acc + fuel_for(+elem), 0);

// part 1
console.log(data);

data2 = fs
  .readFileSync(fileName, "utf-8")
  .trim()
  .split("\n")
  .reduce((acc, elem) => acc + req_fuel(+elem), 0);

console.log(data2);
