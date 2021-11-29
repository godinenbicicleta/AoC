const fs = require("fs");

data = fs
  .readFileSync(process.argv[2], "utf-8")
  .trim()
  .split(",")
  .map((x) => +x);

function process_opcode(opcode, left, right) {
  switch (opcode) {
    case 1:
      return left + right;
    case 2:
      return left * right;
    default:
      console.log(opcode, left, right);
      throw new Error("Invalid Opcode");
  }
}

function run(arr) {
  let position = 0;
  let opcode = arr[position];
  while (opcode != 99) {
    const left_pos = arr[position + 1];
    const right_pos = arr[position + 2];
    const left = arr[left_pos];
    const right = arr[right_pos];

    result = process_opcode(opcode, left, right);
    dest = arr[position + 3];
    arr[dest] = result;
    position = position + 4;
    opcode = arr[position];
  }
  return arr;
}

function p1(...arr) {
  arr[1] = 12;
  arr[2] = 2;
  let res = run(arr);
  return res[0];
}

// part 1:
console.log(p1(...data));

function p2(noun, verb, ...arr) {
  arr[1] = noun;
  arr[2] = verb;
  let res = run(arr);
  return res[0];
}

try {
  console.log(p2(12, 2, ...data));
  for (let noun = 1; noun < 99; noun++) {
    for (let verb = 1; verb < 99; verb++) {
      let res = p2(noun, verb, ...data);
      if (res == 19690720) {
        console.log(100 * noun + verb);
        throw new Error("Run complete");
      }
    }
  }
} catch (error) {
  if (error.message === "Run complete") {
    console.log("done");
  } else {
    throw error;
  }
}
