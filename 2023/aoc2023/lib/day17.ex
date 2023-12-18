defmodule Day17 do
  # 1074 too high
  def main do
    grid = read()

    run(grid, :first)
    |> IO.inspect()

    run(grid, :second)
    |> IO.inspect()
  end

  def run(grid, :second) do
    # heat, x, y, conseq, dir
    queue = [{grid[{1, 0}], 1, 0, 1, ">"}, {grid[{0, 1}], 0, 1, 1, "v"}]
    %{minx: _minx, maxx: maxx, miny: _miny, maxy: maxy} = dimensions(grid)
    goal = {maxx, maxy}

    seen =
      Enum.map(queue, fn {h, x, y, conseq, dir} -> {{x, y, conseq, dir}, h} end)
      |> Enum.into(%{})

    run(queue, goal, grid, seen, :second, 0)
  end

  def run(grid, :first) do
    queue = [{grid[{1, 0}], 1, 0, 1, ">"}, {grid[{0, 1}], 0, 1, 1, "v"}]
    %{minx: _minx, maxx: maxx, miny: _miny, maxy: maxy} = dimensions(grid)
    goal = {maxx, maxy}

    seen =
      Enum.map(queue, fn {_h, x, y, conseq, dir} -> {x, y, conseq, dir} end)
      |> Enum.into(MapSet.new())

    run(queue, goal, grid, seen, :first, 0)
  end

  def insert(current, []) do
    [current]
  end

  def insert(current, [prev | rest]) do
    {h, _, _, _, _} = prev
    {heat, _, _, _, _} = current

    cond do
      h >= heat ->
        [current, prev | rest]

      true ->
        [prev | insert(current, rest)]
    end
  end

  def is_valid_dir(">", "<"), do: false
  def is_valid_dir("<", ">"), do: false
  def is_valid_dir("^", "v"), do: false
  def is_valid_dir("v", "^"), do: false
  def is_valid_dir(_, _), do: true

  def get_conseq(current_c, current_dir, new_dir) do
    if new_dir == current_dir do
      current_c + 1
    else
      1
    end
  end

  def can_stop?({_, _, _, conseq, _}, :second), do: conseq >= 4

  def can_stop?(_, :first), do: true

  def run([current | rest], goal, grid, seen, part, depth) do
    {current_heat, current_x, current_y, current_conseq, current_dir} = current

    if {current_x, current_y} == goal and can_stop?(current, part) do
      current_heat
    else
      candidates =
        [
          {current_x + 1, current_y, ">"},
          {current_x - 1, current_y, "<"},
          {current_x, current_y + 1, "v"},
          {current_x, current_y - 1, "^"}
        ]
        |> Enum.filter(fn {x, y, _} -> grid[{x, y}] != nil end)
        |> Enum.map(fn {x, y, dir} ->
          {current_heat + grid[{x, y}], x, y, get_conseq(current_conseq, current_dir, dir), dir}
        end)
        |> Enum.filter(fn {h, x, y, conseq, dir} ->
          if part == :second do
            seen[{x, y, conseq, dir}] == nil or
              seen[{x, y, conseq, dir}] >= h
          else
            not MapSet.member?(seen, {x, y, conseq, dir})
          end
        end)
        |> Enum.filter(fn {_h, _newx, _newy, _new_conseq, new_dir} ->
          if part == :second do
            cond do
              current_conseq < 4 ->
                new_dir == current_dir

              current_conseq == 10 ->
                new_dir != current_dir and is_valid_dir(new_dir, current_dir)

              true ->
                is_valid_dir(new_dir, current_dir)
            end
          else
            if current_conseq == 3 do
              new_dir != current_dir and is_valid_dir(new_dir, current_dir)
            else
              is_valid_dir(new_dir, current_dir)
            end
          end
        end)

      seen =
        if part == :second do
          Enum.reduce(candidates, seen, fn {h, x, y, conseq, dir}, seen ->
            Map.put(seen, {x, y, conseq, dir}, h)
          end)
        else
          Enum.reduce(candidates, seen, fn {_h, x, y, conseq, dir}, seen ->
            MapSet.put(seen, {x, y, conseq, dir})
          end)
        end

      Enum.reduce(candidates, rest, fn c, r -> insert(c, r) end)
      |> run(goal, grid, seen, part, depth + 1)
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
