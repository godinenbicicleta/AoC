defmodule Day17 do
  # 1074 too high
  def main do
    grid = read()

    run(grid)
    |> IO.inspect()
  end

  def run(grid) do
    queue = [[{0, 0, :right, 0}], [{0, 0, :down, 0}]]
    %{minx: _minx, maxx: maxx, miny: _miny, maxy: maxy} = dimensions(grid)
    goal = {maxx, maxy}
    seen = Map.new([{{0, 0, :right, []}, 0}, {{0, 0, :down, []}, 0}])
    # {run(queue, goal, grid, seen, :first), run(queue, goal, grid, seen, :second)}
    run(queue, goal, grid, seen, :second)
  end

  def insert(path, []) do
    [path]
  end

  def insert(path = [p0 | _], paths) do
    first_path = hd(paths)
    {_, _, _, h} = hd(first_path)
    {_, _, _, heat} = p0

    if h > heat do
      [path | paths]
    else
      [first_path | insert(path, tl(paths))]
    end
  end

  def get_next(path = [head | _rest], grid, seen, part) do
    {x, y, dir, current_heat} = head

    moves =
      case dir do
        :up -> [{x, y - 1, :up}, {x - 1, y, :left}, {x + 1, y, :right}]
        :down -> [{x, y + 1, :down}, {x - 1, y, :left}, {x + 1, y, :right}]
        :left -> [{x, y - 1, :up}, {x - 1, y, :left}, {x, y + 1, :down}]
        :right -> [{x, y - 1, :up}, {x, y + 1, :down}, {x + 1, y, :right}]
      end

    prev =
      path
      |> Enum.take(10)
      |> Enum.map(fn {x, y, dir, _h} -> {x, y, dir} end)

    moves =
      moves
      |> Enum.map(fn {x, y, dir} -> {x, y, dir, grid[{x, y}]} end)
      |> Enum.filter(fn {_, _, _, h} -> h != nil end)
      |> Enum.filter(fn {_, _, dir, _} ->
        if part == :first do
          valid1?(dir, path)
        else
          valid2?(dir, path)
        end
      end)
      |> Enum.filter(fn {x, y, dir, h} ->
        not Map.has_key?(seen, {x, y, dir, prev}) or
          seen[{x, y, dir, prev}] > h + current_heat
      end)

    seen =
      Enum.reduce(moves, seen, fn {x, y, dir, h}, seen ->
        Map.update(seen, {x, y, dir, prev}, h + current_heat, fn existing ->
          max(existing, h + current_heat)
        end)
      end)

    moves = Enum.map(moves, fn {x, y, dir, h} -> [{x, y, dir, h + current_heat} | path] end)
    {moves, seen}
  end

  def valid1?(_dir, []), do: true
  def valid1?(_, [_]), do: true
  def valid1?(_dir, [_, _]), do: true
  def valid1?(d, [{_, _, d, _}, {_, _, d, _}, {_, _, d, _} | _]), do: false
  def valid1?(_, _), do: true

  def valid2?(_dir, []), do: true
  def valid2?(dir, [{_, _, dir, _}]), do: true
  def valid2?(_, [_]), do: false

  def valid2?(dir, path = [head | tail]) do
    {_, _, headdir, _} = head

    prevs =
      path
      |> Enum.take_while(fn {_, _, d, _} -> d == dir end)
      |> Enum.count()

    prevt = tail |> Enum.take_while(fn {_, _, d, _} -> d == headdir end) |> Enum.count()

    valid =
      cond do
        prevs == 10 -> false
        headdir == dir -> true
        prevt < 3 -> false
        true -> true
      end

    valid
  end

  def can_stop([]), do: false

  def can_stop?([h | rest]) do
    {_, _, d, _} = h
    Enum.take_while(rest, fn {_, _, dir, _} -> dir == d end) |> Enum.count() |> Kernel.>=(3)
  end

  def run(paths = [path | rest_paths], goal, grid, seen, part) do
    {x, y, dir, heat} = hd(path)

    if {x, y} == goal and can_stop?(path) do
      #       IO.inspect(Enum.reverse(path))
      heat
    else
      {next_paths, seen} = get_next(path, grid, seen, part)
      paths = Enum.reduce(next_paths, rest_paths, fn next, ps -> insert(next, ps) end)
      run(paths, goal, grid, seen, part)
    end
  end

  def dimensions(grid) do
    minx = Enum.min_by(grid, fn {{x, _y}, _} -> x end) |> elem(0) |> elem(0)
    maxx = Enum.max_by(grid, fn {{x, _y}, _} -> x end) |> elem(0) |> elem(0)
    miny = Enum.min_by(grid, fn {{_x, y}, _} -> y end) |> elem(0) |> elem(1)
    maxy = Enum.max_by(grid, fn {{_x, y}, _} -> y end) |> elem(0) |> elem(1)
    %{minx: minx, maxx: maxx, miny: miny, maxy: maxy}
  end

  def read() do
    File.stream!("data/day17.txt")
    |> Enum.map(fn line ->
      String.trim(line)
      |> String.split("", trim: true)
      |> Enum.with_index()
    end)
    |> Enum.with_index()
    |> Enum.map(fn {row, y} -> Enum.map(row, fn {v, x} -> {{x, y}, String.to_integer(v)} end) end)
    |> Enum.concat()
    |> Enum.into(%{})
  end
end
