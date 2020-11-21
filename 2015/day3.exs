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

initial = MapSet.new([{0, 0}])
acc0 = {initial, {{0, 0}, {0, 0}}}

map = fn
  n when rem(n, 2) == 0 -> :santa
  _ -> :robot
end

move2 = fn
  {"^", index}, {pos, {{xsanta, ysanta}, {xrobot, yrobot}}} ->
    case map.(index) do
      :santa ->
        new_pos = {santa_pos, _robot_pos} = {{xsanta, ysanta + 1}, {xrobot, yrobot}}
        {MapSet.put(pos, santa_pos), new_pos}

      :robot ->
        new_pos = {_santa_pos, robot_pos} = {{xsanta, ysanta}, {xrobot, yrobot + 1}}
        {MapSet.put(pos, robot_pos), new_pos}
    end

  {"v", index}, {pos, {{xsanta, ysanta}, {xrobot, yrobot}}} ->
    case map.(index) do
      :santa ->
        new_pos = {santa_pos, _robot_pos} = {{xsanta, ysanta - 1}, {xrobot, yrobot}}
        {MapSet.put(pos, santa_pos), new_pos}

      :robot ->
        new_pos = {_santa_pos, robot_pos} = {{xsanta, ysanta}, {xrobot, yrobot - 1}}
        {MapSet.put(pos, robot_pos), new_pos}
    end

  {">", index}, {pos, {{xsanta, ysanta}, {xrobot, yrobot}}} ->
    case map.(index) do
      :santa ->
        new_pos = {santa_pos, _robot_pos} = {{xsanta + 1, ysanta}, {xrobot, yrobot}}
        {MapSet.put(pos, santa_pos), new_pos}

      :robot ->
        new_pos = {_santa_pos, robot_pos} = {{xsanta, ysanta}, {xrobot + 1, yrobot}}
        {MapSet.put(pos, robot_pos), new_pos}
    end

  {"<", index}, {pos, {{xsanta, ysanta}, {xrobot, yrobot}}} ->
    case map.(index) do
      :santa ->
        new_pos = {santa_pos, _robot_pos} = {{xsanta - 1, ysanta}, {xrobot, yrobot}}
        {MapSet.put(pos, santa_pos), new_pos}

      :robot ->
        new_pos = {_santa_pos, robot_pos} = {{xsanta, ysanta}, {xrobot - 1, yrobot}}
        {MapSet.put(pos, robot_pos), new_pos}
    end
end

File.read!("day3.txt")
|> String.trim()
|> String.split("", trim: true)
|> Enum.with_index()
|> Enum.reduce(acc0, move2)
|> elem(0)
|> MapSet.size()
|> IO.inspect()
