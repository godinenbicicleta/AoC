to_area = fn x, acc ->
  [l, w, h] = String.split(x, "x") |> Enum.map(&String.to_integer/1)
  lw = l * w
  lh = l * h
  hw = w * h
  min = Enum.min([lw, lh, hw])
  2 * (lw + lh + hw) + min + acc
end

to_ribbon = fn x, acc ->
  [l, w, h] =
    String.split(x, "x")
    |> Enum.map(&String.to_integer/1)
    |> Enum.sort()

  perimeter = 2 * l + 2 * w
  extra = l * w * h
  perimeter + extra + acc
end

File.read!("day2.txt")
|> String.trim()
|> String.split("\n", trim: true)
|> Enum.reduce(0, to_area)
|> IO.inspect()

File.read!("day2.txt")
|> String.trim()
|> String.split("\n", trim: true)
|> Enum.reduce(0, to_ribbon)
|> IO.inspect()
