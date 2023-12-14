defmodule Day14 do
  @max_cycles 1_000_000_000

  def p2 do
    grid = read()

    {seen, grid, cycle} =
      Enum.reduce_while(1..@max_cycles, {grid, %{grid: 0}}, fn cycle, {grid, seen} ->
        res =
          [:north, :west, :south, :east]
          |> Enum.reduce(grid, &do_update(&2, &1))

        if Map.get(seen, res) do
          {:halt, {seen, res, cycle}}
        else
          seen = Map.put(seen, res, cycle)
          {:cont, {res, seen}}
        end
      end)

    first = seen[grid]
    cycle_size = cycle - first

    ix =
      rem(@max_cycles - first, cycle_size)

    Enum.find(seen, fn {_g, v} -> v == ix + first end) |> elem(0) |> get_load()
  end

  def main do
    grid = read()

    grid
    |> do_update(:north)
    |> get_load()
    |> IO.inspect(label: "p1")

    {_, map} =
      Enum.reduce(1..200, {grid, %{}}, fn cycle, {grid, seen} ->
        res =
          [:north, :west, :south, :east]
          |> Enum.reduce(grid, &do_update(&2, &1))

        load = get_load(res)
        seen = Map.update(seen, load, [cycle], fn prev -> [cycle | prev] end)

        {res, seen}
      end)

    map = map |> Enum.filter(fn {_k, v} -> tl(v) != [] end) |> Enum.into(%{})

    cycle_size =
      map
      |> Enum.map(fn {_k, vs} ->
        Enum.chunk_every(vs, 2, 1, :discard)
        |> Enum.map(fn [left, right] -> left - right end)
      end)
      |> Enum.filter(fn diffs -> Enum.all?(diffs, fn d -> d == hd(diffs) end) end)
      |> hd
      |> hd

    Enum.reduce_while(1..@max_cycles, rem(@max_cycles, cycle_size), fn _, acc ->
      case Enum.find(map, fn {_k, vs} -> acc in vs end) do
        nil -> {:cont, acc + cycle_size}
        {k, _} -> {:halt, k}
      end
    end)
    |> IO.inspect(label: "p2")
  end

  def do_update(grid, dir) do
    sort_func =
      case dir do
        :north -> fn {x, y} -> {y, x} end
        :south -> fn {x, y} -> {-y, x} end
        :east -> fn {x, y} -> {-x, y} end
        :west -> fn {x, y} -> {x, y} end
      end

    grid
    |> Map.keys()
    |> Enum.sort_by(sort_func)
    |> Enum.reduce(grid, fn elem, acc -> reducer(elem, acc, dir) end)
  end

  def get_load(grid) do
    maxy =
      grid
      |> Enum.max_by(fn {{_x, y}, _v} -> y end)
      |> elem(0)
      |> elem(1)
      |> Kernel.+(1)

    grid
    |> Stream.filter(fn {_p, v} -> v == "O" end)
    |> Enum.reduce(0, fn {{_x, y}, _v}, acc -> acc + maxy - y end)
  end

  def reducer(pos, grid, dir) do
    case grid[pos] do
      "#" -> grid
      "." -> grid
      "O" -> update(grid, pos, dir)
    end
  end

  def printg(grid) do
    Map.keys(grid)
    |> Enum.sort_by(fn {x, y} -> {y, x} end)
    |> Enum.reduce({[], [], 0}, fn {x, y}, {arr, row, j} ->
      v = grid[{x, y}]

      if y == j do
        {arr, [v | row], j}
      else
        row = Enum.reverse(row)
        arr = [row | arr]
        {arr, [v], j + 1}
      end
    end)
    |> then(fn {acc, row, _} ->
      Enum.reverse([
        Enum.reverse(row) | acc
      ])
    end)
    |> Enum.join("\n")
    |> IO.puts()

    IO.puts("\n")
  end

  def update(grid, pos = {x, y}, dir) do
    next_pos =
      case dir do
        :north -> {x, y - 1}
        :west -> {x - 1, y}
        :south -> {x, y + 1}
        :east -> {x + 1, y}
      end

    next_value = grid[next_pos]

    if next_value in [nil, "#", "O"] do
      grid
    else
      grid
      |> Map.put(next_pos, "O")
      |> Map.put(pos, ".")
      |> update(next_pos, dir)
    end
  end

  def read do
    File.stream!("data/day14.txt")
    |> Enum.map(fn line ->
      line
      |> String.trim()
      |> String.codepoints()
      |> Enum.with_index()
    end)
    |> Stream.with_index()
    |> Stream.map(fn {line, y} -> Enum.map(line, fn {v, x} -> {{x, y}, v} end) end)
    |> Stream.concat()
    |> Enum.into(%{})
  end
end
