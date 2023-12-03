defmodule Day03 do
  def p1 do
    File.stream!("data/day03.txt")
    |> Enum.map(&String.trim/1)
    |> Enum.with_index()
    |> Enum.map(&parse/1)
    |> List.flatten()
    |> Enum.into(%{}, fn {v, y, x} -> {{x, y}, v} end)
    |> sum
  end

  def p2 do
    File.stream!("data/day03.txt")
    |> Enum.map(&String.trim/1)
    |> Enum.with_index()
    |> Enum.map(&parse/1)
    |> List.flatten()
    |> Enum.into(%{}, fn {v, y, x} -> {{x, y}, v} end)
    |> sum_gears
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

  def is_part_number({x, y}, m) do
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
    |> Enum.any?(fn key ->
      Map.get(m, key, ".") != "." and not is_num(Map.get(m, key))
    end)
  end

  def reducer({{x, y}, v}, {m, seen, total} = acc) do
    if not is_part_number({x, y}, m) or MapSet.member?(seen, {x, y}) do
      acc
    else
      {num, coords} = build_num({x, y}, v, m)
      {m, MapSet.union(coords, seen), total + num}
    end
  end

  def get_nums({x, y}, m) do
    nums = []
    seen = MapSet.new()

    {nums, seen} =
      if is_num(Map.get(m, {x - 1, y - 1}, ".")) and not MapSet.member?(seen, {x - 1, y - 1}) do
        {n, coords} = build_num({x - 1, y - 1}, m[{x - 1, y - 1}], m)
        {[n | nums], MapSet.union(seen, coords)}
      else
        {nums, seen}
      end

    {nums, seen} =
      if is_num(Map.get(m, {x + 1, y + 1}, ".")) and not MapSet.member?(seen, {x + 1, y + 1}) do
        {n, coords} = build_num({x + 1, y + 1}, m[{x + 1, y + 1}], m)
        {[n | nums], MapSet.union(seen, coords)}
      else
        {nums, seen}
      end

    {nums, seen} =
      if is_num(Map.get(m, {x + 1, y - 1}, ".")) and not MapSet.member?(seen, {x + 1, y - 1}) do
        {n, coords} = build_num({x + 1, y - 1}, m[{x + 1, y - 1}], m)
        {[n | nums], MapSet.union(seen, coords)}
      else
        {nums, seen}
      end

    {nums, seen} =
      if is_num(Map.get(m, {x - 1, y + 1}, ".")) and not MapSet.member?(seen, {x - 1, y + 1}) do
        {n, coords} = build_num({x - 1, y + 1}, m[{x - 1, y + 1}], m)
        {[n | nums], MapSet.union(seen, coords)}
      else
        {nums, seen}
      end

    {nums, seen} =
      if is_num(Map.get(m, {x - 1, y}, ".")) and not MapSet.member?(seen, {x - 1, y}) do
        {n, coords} = build_num({x - 1, y}, m[{x - 1, y}], m)
        {[n | nums], MapSet.union(seen, coords)}
      else
        {nums, seen}
      end

    {nums, seen} =
      if is_num(Map.get(m, {x + 1, y}, ".")) and not MapSet.member?(seen, {x + 1, y}) do
        {n, coords} = build_num({x + 1, y}, m[{x + 1, y}], m)
        {[n | nums], MapSet.union(seen, coords)}
      else
        {nums, seen}
      end

    {nums, seen} =
      if is_num(Map.get(m, {x, y + 1}, ".")) and not is_num(Map.get(m, {x + 1, y + 1}, ".")) and
           not is_num(Map.get(m, {x - 1, y + 1}, ".")) and not MapSet.member?(seen, {x, y + 1}) do
        {n, coords} = build_num({x, y + 1}, m[{x, y + 1}], m)
        {[n | nums], MapSet.union(seen, coords)}
      else
        {nums, seen}
      end

    {nums, seen} =
      if is_num(Map.get(m, {x, y - 1}, ".")) and not is_num(Map.get(m, {x + 1, y - 1}, ".")) and
           not is_num(Map.get(m, {x - 1, y - 1}, ".")) and not MapSet.member?(seen, {x, y - 1}) do
        {n, coords} = build_num({x, y - 1}, m[{x, y - 1}], m)
        {[n | nums], MapSet.union(seen, coords)}
      else
        {nums, seen}
      end

    nums
  end

  def reduce_gears({{x, y}, _}, {m, total} = acc) do
    any_num =
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
      |> Enum.any?(fn k -> Map.get(m, k, ".") |> is_num end)

    if any_num do
      nums = get_nums({x, y}, m)

      nums_prod =
        if length(nums) == 2 do
          [a, b] = nums
          a * b
        else
          0
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
      Enum.map(left, fn x -> elem(x, 0) end) ++ [v] ++ Enum.map(right, fn x -> elem(x, 0) end)

    num =
      Enum.join(num_list)
      |> String.to_integer()

    coords =
      Enum.map(left, fn x -> elem(x, 1) end) ++
        [{x, y}] ++ Enum.map(right, fn x -> elem(x, 1) end)

    {num, MapSet.new(coords)}
  end
end
