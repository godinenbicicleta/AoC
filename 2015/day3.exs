initial = MapSet.new([{0, 0}])
acc0 = {initial, {0, 0}}

move = fn
  "^", {positions, {x, y}} ->
    pos = {x, y + 1}
    new_positions = MapSet.put(positions, pos)
    {new_positions, pos}

  "v", {positions, {x, y}} ->
    pos = {x, y - 1}
    new_positions = MapSet.put(positions, pos)
    {new_positions, pos}

  ">", {positions, {x, y}} ->
    pos = {x + 1, y}
    new_positions = MapSet.put(positions, pos)
    {new_positions, pos}

  "<", {positions, {x, y}} ->
    pos = {x - 1, y}
    new_positions = MapSet.put(positions, pos)
    {new_positions, pos}
end

File.read!("day3.txt")
|> String.trim()
|> String.split("", trim: true)
|> Enum.reduce(acc0, move)
|> elem(0)
|> MapSet.size()
|> IO.inspect()
