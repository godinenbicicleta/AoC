defmodule Day03 do
  def preprocess(fname) do
    fname
    |> File.stream!()
    |> Enum.map(&String.trim/1)
    |> Enum.with_index()
    |> Enum.map(&parse/1)
    |> List.flatten()
    |> Enum.into(%{}, fn {v, y, x} -> {{x, y}, v} end)
  end

  def p1 do
    "data/day03.txt"
    |> preprocess
    |> sum
  end

  def p2 do
    "data/day03.txt"
    |> preprocess
    |> sum_gears
  end

  def neighbors({x, y}) do
    [
      {x - 1, y - 1},
      {x - 1, y + 1},
      {x + 1, y - 1},
      {x + 1, y + 1},
      {x + 1, y},
      {x - 1, y},
      {x, y + 1},
      {x, y - 1}
    ]
  end

  def parse({line, ix}) do
    line
    |> String.split("", trim: true)
    |> Enum.with_index()
    |> Enum.map(fn {x, i} -> {x, ix, i} end)
  end

  def is_num(s) do
    Integer.parse(s) != :error
  end

  def sum_gears(m) do
    Enum.filter(m, fn {_k, v} -> v == "*" end)
    |> Enum.into(%{})
    |> Enum.reduce({m, 0}, &reduce_gears/2)
    |> elem(1)
  end

  def sum(m) do
    Enum.filter(m, fn {_k, v} -> is_num(v) end)
    |> Enum.into(%{})
    |> Enum.reduce({m, MapSet.new(), 0}, &reducer/2)
    |> elem(2)
  end

  def is_part_number(x, m) do
    x
    |> neighbors
    |> Enum.any?(fn key ->
      v = Map.get(m, key, ".")
      v != "." and not is_num(v)
    end)
  end

  def reducer({x, v}, {m, seen, total} = acc) do
    if not is_part_number(x, m) or MapSet.member?(seen, x) do
      acc
    else
      {num, coords} = build_num(x, v, m)
      {m, MapSet.union(coords, seen), total + num}
    end
  end

  def get_nums(x, m) do
    x
    |> neighbors
    |> Enum.reduce({[], MapSet.new()}, fn c, {nums, seen} ->
      v = Map.get(m, c, ".")

      if is_num(v) and not MapSet.member?(seen, c) do
        {n, coords} = build_num(c, m[c], m)
        {[n | nums], MapSet.union(seen, coords)}
      else
        {nums, seen}
      end
    end)
    |> elem(0)
  end

  def reduce_gears({x, _}, {m, total} = acc) do
    any_num =
      x
      |> neighbors
      |> Enum.any?(fn k -> Map.get(m, k, ".") |> is_num end)

    if any_num do
      nums = get_nums(x, m)

      nums_prod =
        case nums do
          [a, b] -> a * b
          _ -> 0
        end

      {m, total + nums_prod}
    else
      acc
    end
  end

  def build_num({x, y}, v, m) do
    left =
      Enum.reduce_while([1, 2], [], fn d, acc ->
        n = Map.get(m, {x - d, y}, ".")

        if is_num(n) do
          {:cont, [{n, {x - d, y}} | acc]}
        else
          {:halt, acc}
        end
      end)

    right =
      Enum.reduce_while([1, 2], [], fn d, acc ->
        n = Map.get(m, {x + d, y}, ".")

        if is_num(n) do
          {:cont, [{n, {x + d, y}} | acc]}
        else
          {:halt, acc}
        end
      end)
      |> Enum.reverse()

    num_list =
      Enum.map(left, &elem(&1, 0)) ++ [v] ++ Enum.map(right, &elem(&1, 0))

    num =
      Enum.join(num_list)
      |> String.to_integer()

    coords =
      Enum.map(left, &elem(&1, 1)) ++
        [{x, y}] ++ Enum.map(right, &elem(&1, 1))

    {num, MapSet.new(coords)}
  end
end
