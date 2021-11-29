"use strict";
const fs = require("fs");
const readline = require("readline");
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

let input = undefined;

const data = fs.readFileSync(process.argv[2], "utf-8").trim().split(",");
console.log(data);

function run(...arr) {
  let currentPos = 0;
  while (true) {
    const raw_opcode = arr[currentPos];
    let intOpcode = raw_opcode.slice(raw_opcode.length - 2, raw_opcode.length);
    intOpcode = +intOpcode;
    console.log(intOpcode);

    if (intOpcode === 99) return console.log("Halted", arr.slice(0, 5));
    if (intOpcode === 4) {
      const parameter_mode = raw_opcode[raw_opcode.length - 3] || 0;
      const parameter = arr[currentPos + 1];
      if (parameter_mode === 0) console.log(arr[parameter]);
      else console.log(parameter);
      currentPos += 2;
      continue;
    }
    if (intOpcode === 3) {
      console.log(raw_opcode);
      const parameter_mode = raw_opcode[raw_opcode.length - 3] || 0;
      const parameter = arr[currentPos + 1];
      console.log("Here");
      rl.question("User input: ", (i) => {
        // input = i;
        console.log(i);
        rl.close();
      });
      arr[+parameter] = input;
      continue;
    }
    if (intOpcode === 1) {
      const parameter_mode1 = raw_opcode[raw_opcode.length - 3] || 0;
      const parameter1 = +arr[currentPos + 1];

      const parameter_mode2 = raw_opcode[raw_opcode.length - 4] || 0;
      const parameter2 = +arr[currentPos + 2];

      let left = parameter_mode1 === 0 ? arr[parameter1] : parameter1;
      let right = parameter_mode2 === 0 ? arr[parameter2] : parameter2;

      arr[+arr[currentPos + 3]] = left + right;

      currentPos += 4;
      continue;
    }

    if (intOpcode === 2) {
      const parameter_mode1 = raw_opcode[raw_opcode.length - 3] || 0;
      const parameter1 = +arr[currentPos + 1];

      const parameter_mode2 = raw_opcode[raw_opcode.length - 4] || 0;
      const parameter2 = +arr[currentPos + 2];

      let left = parameter_mode1 === 0 ? arr[parameter1] : parameter1;
      let right = parameter_mode2 === 0 ? arr[parameter2] : parameter2;

      arr[+arr[currentPos + 3]] = left * right;

      currentPos += 4;
      continue;
    }

    throw new Error("Invalid opcode", intOpcode);
  }
}

run(...["3", "0", "4", "0", "99"]);
