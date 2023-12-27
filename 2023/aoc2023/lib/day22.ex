defmodule Day22 do
  def main do
    p1()
  end

  def p1() do
    briqs = read() |> run

    briqs
    |> Enum.map(fn b ->
      without = Enum.reject(briqs, fn br -> br == b end)

      new = without |> run

      collapsed_new = new |> collapse

      if collapsed_new == collapse(without), do: {1, 0}, else: {0, diff(new, without)}
    end)
    |> Enum.reduce({0, 0}, fn {x, y}, {a, b} -> {x + a, y + b} end)
  end

  def diff(left, right) do
    Enum.reduce(left, 0, fn row, total ->
      total + if Enum.any?(right, fn r -> r == row end), do: 0, else: 1
    end)
  end

  def collapse(briqs) do
    Enum.reduce(briqs, MapSet.new(), fn b, acc -> MapSet.union(b, acc) end)
  end

  def run(briqs) do
    briqs
    |> Enum.reduce([], &insert/2)
    |> Enum.sort_by(fn briq ->
      minz = Enum.min_by(briq, fn {_, _, z} -> z end) |> elem(2)
      miny = Enum.min_by(briq, fn {_, y, _z} -> y end) |> elem(1)
      minx = Enum.min_by(briq, fn {x, _, _z} -> x end) |> elem(0)
      {minz, miny, minx}
    end)
  end

  def insert(b, []) do
    case min_max_z(b) do
      {1, _} -> [b]
      _ -> [move_down(b)]
    end
  end

  def insert(briq, briqs) do
    down = move_down(briq)
    union = Enum.reduce(briqs, MapSet.new(), fn x, acc -> MapSet.union(acc, x) end)
    minz = min_max_z(briq) |> elem(0)

    disjoint = MapSet.disjoint?(down, union)

    cond do
      disjoint and minz > 1 ->
        insert(down, briqs)

      true ->
        [briq | briqs]
    end
  end

  def move_down(points) do
    Enum.map(points, fn {x, y, z} -> {x, y, max(z - 1, 1)} end) |> Enum.into(MapSet.new())
  end

  def min_max_z(points) do
    {mi, ma} = Enum.min_max_by(points, fn {_x, _y, z} -> z end)
    {elem(mi, 2), elem(ma, 2)}
  end

  def read() do
    File.stream!("data/day22_test.txt")
    |> Enum.map(fn line ->
      line
      |> String.trim()
      |> String.split("~")
      |> Enum.map(&String.split(&1, ","))
      |> Enum.zip()
      |> Enum.map(fn {s, e} -> String.to_integer(s)..String.to_integer(e) end)
    end)
    |> Enum.sort_by(fn [_x, _y, z] -> z end)
    |> Enum.map(fn [rx, ry, rz] ->
      for x <- rx, y <- ry, z <- rz, into: MapSet.new() do
        {x, y, z}
      end
    end)
  end
end
