defmodule Lights do
  def read do
    File.read!("day18.txt")
    |> String.trim()
    |> String.split("\n", trim: true)
    |> Stream.map(&String.graphemes/1)
    |> Stream.map(&Enum.with_index/1)
    |> Stream.with_index()
    |> Stream.flat_map(&to_tuple/1)
    |> Enum.into(%{})
    |> IO.inspect()
  end

  def solve(steps) do
    map = read()
    IO.puts("initial state")
    print(map)
    map = %{map | {0, 0} => "#", {0, 99} => "#", {99, 0} => "#", {99, 99} => "#"}

    map
    |> move(steps)
  end

  def move(map, 0) do
    map
  end

  def move(map, steps) do
    move(map)
    |> move(steps - 1)
  end

  def move(map) do
    new_map =
      for y <- 0..99, x <- 0..99, into: %{} do
        {{y, x}, update({y, x}, map)}
      end

    IO.puts("")
    print(new_map)
    IO.puts("")
    new_map
  end

  def update({0, 0}, _) do
    "#"
  end

  def update({0, 99}, _) do
    "#"
  end

  def update({99, 0}, _) do
    "#"
  end

  def update({99, 99}, _) do
    "#"
  end

  def update(c = {_x, _y}, map) do
    nb = neighbors(c, map)

    case Map.get(map, c) do
      "#" ->
        case Enum.count(nb, fn x -> x == "#" end) do
          2 -> "#"
          3 -> "#"
          _ -> "."
        end

      "." ->
        case Enum.count(nb, fn x -> x == "#" end) do
          3 -> "#"
          _ -> "."
        end
    end
  end

  def neighbors({x, y}, map) do
    [
      {x + 1, y},
      {x - 1, y},
      {x + 1, y + 1},
      {x - 1, y + 1},
      {x, y + 1},
      {x, y - 1},
      {x + 1, y - 1},
      {x - 1, y - 1}
    ]
    |> Enum.filter(fn {x, y} -> x >= 0 and y >= 0 and x <= 99 and y <= 99 end)
    |> Enum.map(&Map.get(map, &1))
  end

  def to_tuple({line, ix}) do
    Enum.map(line, fn {ch, i} -> {{i, ix}, ch} end)
  end

  def count(map) do
    map
    |> Enum.count(fn {_, y} -> y == "#" end)
  end

  def print(map) do
    for y <- 0..99 do
      for x <- 0..99 do
        IO.write(Map.get(map, {x, y}))
      end

      IO.write("\n")
    end
  end
end

# 390 too low
Lights.solve(100)
|> Enum.count(fn {_, y} -> y == "#" end)
|> IO.inspect()
