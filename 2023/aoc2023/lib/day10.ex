defmodule Day10 do
  def main do
    grid = parse_grid("data/day10.txt")

    s =
      grid
      |> Enum.find(&(elem(&1, 1) == "S"))
      |> elem(0)

    loop = solve(s, grid) |> hd

    loop
    |> hd
    |> elem(2)
    |> div(2)
    |> IO.inspect(label: "p1")

    [_, left] = loop |> Enum.take(2)
    left = elem(left, 0)
    [_, right] = Enum.reverse(loop) |> Enum.take(2)
    right = elem(right, 0)

    grid = replace_s(grid, s, left, right)

    loop_pos = loop_set(loop)

    %{maxx: maxx} =
      dimensions(grid)

    grid
    |> Enum.reject(fn {coord, _} -> MapSet.member?(loop_pos, coord) end)
    |> Enum.map(fn {coord, _} ->
      {x, y} = coord

      res =
        Enum.reduce(x..maxx, [], fn newx, acc ->
          cond do
            grid[{newx, y}] == "-" -> acc
            MapSet.member?(loop_pos, {newx, y}) -> [grid[{newx, y}] | acc]
            true -> acc
          end
        end)

      Enum.reverse(res)
    end)
    |> Enum.count(&inside?/1)
    |> IO.inspect(label: "p2")
  end

  def parse_grid(fname) do
    fname
    |> File.stream!()
    |> Enum.map(fn line ->
      line
      |> String.trim()
      |> String.codepoints()
      |> Enum.with_index()
    end)
    |> Enum.with_index()
    |> Enum.map(fn {line, y} ->
      Enum.map(line, fn {c, x} ->
        {{x, y}, c}
      end)
    end)
    |> List.flatten()
    |> Enum.into(%{})
  end

  def replace_s(grid, s, left, right) do
    {x, y} = s
    {x1, y1} = left
    {x2, y2} = right

    rep =
      cond do
        x1 == x2 -> "|"
        y1 == y2 -> "-"
        (x1 > x or x2 > x) and (y1 > y or y2 > y) -> "F"
        (x1 > x or x2 > x) and (y1 < y or y2 < y) -> "L"
        (x1 < x or x2 < x) and (y1 < y or y2 < y) -> "J"
        (x1 < x or x2 < x) and (y1 > y or y2 > y) -> "7"
      end

    Map.put(grid, s, rep)
  end

  def inside?(arr), do: inside?(arr, 0)
  def inside?([], acc), do: rem(acc, 2) == 1
  def inside?([_], acc), do: rem(acc + 1, 2) == 1
  def inside?(["|" | rest], acc), do: inside?(rest, acc + 1)

  def inside?([a, b | rest], acc) do
    case {a, b} do
      {"L", "J"} -> inside?(rest, acc)
      {"L", "7"} -> inside?(rest, acc + 1)
      {"L", "F"} -> throw(:here)
      {"J", "L"} -> inside?(rest, acc)
      {"J", "7"} -> throw(:here1)
      {"J", "F"} -> inside?(rest, acc)
      {"7", "L"} -> inside?(rest, acc)
      {"7", "J"} -> throw(:here2)
      {"7", "F"} -> inside?(rest, acc)
      {"F", "L"} -> throw(:here3)
      {"F", "J"} -> inside?(rest, acc + 1)
      {"F", "7"} -> inside?(rest, acc)
    end
  end

  def dimensions(grid) do
    minx = Enum.min_by(grid, fn {{x, _}, _} -> x end) |> elem(0) |> elem(0)
    miny = Enum.min_by(grid, fn {{_, y}, _} -> y end) |> elem(0) |> elem(1)
    maxx = Enum.max_by(grid, fn {{x, _}, _} -> x end) |> elem(0) |> elem(0)
    maxy = Enum.max_by(grid, fn {{_, y}, _} -> y end) |> elem(0) |> elem(1)
    %{minx: minx, maxx: maxx, miny: miny, maxy: maxy}
  end

  def loop_set(loop) do
    Enum.map(loop, fn {p, _, _} -> p end) |> Enum.into(MapSet.new())
  end

  def solve(s, grid) do
    neighbors(s, grid)
    |> Enum.map(fn n -> [{n, 1}, {s, 0}] end)
    |> Enum.map(&run(&1, grid, s))
  end

  def run(path = [{goal, _steps} | _], grid, goal) do
    path
    |> Enum.map(fn {pos, steps} -> {pos, grid[pos], steps} end)
  end

  def run(path = [{next, steps}, {prev, _} | _], grid, goal) do
    Enum.find(
      neighbors(next, grid[next], grid)
      |> Enum.filter(fn x -> x != prev end)
      |> Enum.map(fn n -> [{n, steps + 1} | path] end)
      |> Enum.map(&run(&1, grid, goal)),
      fn x -> x != [] end
    )
  end

  def valid?(k = {_x, _y}, grid) do
    case Map.get(grid, k) do
      "." -> false
      nil -> false
      _ -> true
    end
  end

  def neighbors({x, y}, g) do
    [{x - 1, y}, {x + 1, y}, {x, y - 1}, {x, y + 1}]
    |> Enum.filter(&valid?(&1, g))
    |> Enum.filter(fn {i, j} ->
      case g[{i, j}] do
        "|" -> i == x
        "-" -> j == y
        "L" -> (i == x - 1 and j == y) or (j == y + 1 and i == x)
        "J" -> (i == x + 1 and j == y) or (j == y + 1 and i == x)
        "7" -> (i == x + 1 and j == y) or (j == y - 1 and i == x)
        "F" -> (i == x - 1 and j == y) or (j == y - 1 and i == x)
      end
    end)
  end

  def neighbors({x, y}, current, g) do
    ns =
      case current do
        "|" -> [{x, y + 1}, {x, y - 1}]
        "-" -> [{x + 1, y}, {x - 1, y}]
        "L" -> [{x + 1, y}, {x, y - 1}]
        "J" -> [{x - 1, y}, {x, y - 1}]
        "7" -> [{x, y + 1}, {x - 1, y}]
        "F" -> [{x, y + 1}, {x + 1, y}]
      end

    ns |> Enum.filter(&valid?(&1, g))
  end
end
