const [start, end] = [356261, 846303];

function isValid(password) {
  const p = password.toString();
  if (p.length !== 6) return false;

  const adjacent = [...p].reduce((prev, current) => {
    if (prev === true) return true;
    if (prev === current) return true;
    return current;
  });

  if (!(adjacent === true)) return false;

  const nonDecreasing = [...p].reduce((prev, current) => {
    if (prev === false) return false;
    if (+prev > +current) return false;
    return current;
  });

  if (nonDecreasing === false) return false;
  return true;
}

function isValid2(p) {
  password = p.toString();
  for (let i = 0; i < password.length; i++) {
    if (
      password[i] == password[i + 1] &&
      password[i + 1] != password[i + 2] &&
      password[i - 1] != password[i]
    )
      return true;
  }
  return false;
}

// part 1

function countValid() {
  let count1 = 0;
  let count2 = 0;

  for (let num = start; num <= end; num++) {
    if (isValid(num)) {
      count1++;
      if (isValid2(num)) count2++;
    }
  }
  return [count1, count2];
}

console.log(countValid());
