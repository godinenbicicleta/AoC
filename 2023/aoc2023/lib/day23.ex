defmodule Day23 do
  def main do
    p1() |> IO.inspect()
    p2()
  end

  def p1 do
    grid = read()
    start = {1, 0}
    maxx = Enum.max_by(grid, fn {{x, _y}, _v} -> x end) |> elem(0) |> elem(0)
    maxy = Enum.max_by(grid, fn {{_x, y}, _v} -> y end) |> elem(0) |> elem(1)
    goal = {maxx - 1, maxy}

    paths = run(grid, [[start]], goal, [])
    Enum.map(paths, fn p -> length(p) - 1 end) |> Enum.max()
  end

  def p2 do
    grid = read()
    start = {1, 0}
    maxx = Enum.max_by(grid, fn {{x, _y}, _v} -> x end) |> elem(0) |> elem(0)
    maxy = Enum.max_by(grid, fn {{_x, y}, _v} -> y end) |> elem(0) |> elem(1)
    goal = {maxx - 1, maxy}

    run2(grid, [{start, MapSet.new([start])}], goal, -1)
  end

  def run2(_grid, [], _goal, maxpath), do: maxpath

  def run2(grid, [{{x, y}, seen} | queue], {x, y}, maxpath) do
    run2(grid, queue, {x, y}, max(MapSet.size(seen) - 1, maxpath))
  end

  def run2(grid, [{{x, y}, seen} | queue], goal, maxpath) do
    candidates =
      [{x + 1, y}, {x - 1, y}, {x, y + 1}, {x, y - 1}]

    candidates =
      candidates
      |> Enum.reject(fn {x, y} -> grid[{x, y}] == nil end)
      |> Enum.reject(fn {x, y} -> grid[{x, y}] == "#" end)
      |> Enum.reject(fn {x, y} -> MapSet.member?(seen, {x, y}) end)

    candidates = candidates |> Enum.map(fn {i, j} -> {{i, j}, MapSet.put(seen, {i, j})} end)

    queue = candidates ++ queue

    run2(grid, queue, goal, maxpath)
  end

  def run(_grid, [], _goal, sols), do: sols

  def run(grid, [p = [{x, y} | _] | queue], {x, y}, sols) do
    run(grid, queue, {x, y}, [p | sols])
  end

  def run(grid, [c = [{x, y} | p] | queue], goal, sols) do
    candidates =
      case grid[{x, y}] do
        "." -> [{x + 1, y}, {x - 1, y}, {x, y + 1}, {x, y - 1}]
        "v" -> [{x, y + 1}]
        ">" -> [{x + 1, y}]
        "<" -> [{x - 1, y}]
        "^" -> [{x, y - 1}]
      end

    candidates =
      candidates
      |> Enum.reject(fn {x, y} -> grid[{x, y}] == nil end)
      |> Enum.reject(fn {x, y} -> grid[{x, y}] == "#" end)
      |> Enum.reject(fn {x, y} -> {x, y} in p end)

    candidates = candidates |> Enum.map(fn {x, y} -> [{x, y} | c] end)

    queue = candidates ++ queue

    run(grid, queue, goal, sols)
  end

  def read do
    File.stream!("data/day23.txt")
    |> Enum.map(fn line ->
      line
      |> String.trim()
      |> String.split("", trim: true)
      |> Enum.with_index()
    end)
    |> Enum.with_index()
    |> Enum.map(fn {row, y} -> Enum.map(row, fn {v, x} -> {{x, y}, v} end) end)
    |> Enum.concat()
    |> Enum.into(%{})
  end
end
