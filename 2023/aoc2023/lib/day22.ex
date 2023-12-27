defmodule Day22 do
  def main do
    p1()
  end

  def p1() do
    {briqs, _moved} = read() |> run

    briqs
    |> Enum.with_index()
    |> Enum.map(fn {_briq, index} ->
      without =
        List.delete_at(briqs, index)

      {_new, moved} =
        run(without)

      if moved == 0, do: {1, 0}, else: {0, moved}
    end)
    |> Enum.reduce({0, 0}, fn {x, y}, {a, b} -> {a + x, y + b} end)
  end

  def run(briqs) do
    {b, m} =
      briqs
      |> Enum.reduce(
        {[], 0},
        fn briq, {briqs, total} ->
          {new_briq, new_briqs} = insert(briq, briqs)
          if new_briq == briq, do: {new_briqs, total}, else: {new_briqs, total + 1}
        end
      )

    {Enum.reverse(b), m}
  end

  def insert(b, []) do
    case min_max_z(b) do
      {1, _} -> {b, [b]}
      _ -> insert(move_down(b), [])
    end
  end

  def insert(briq, briqs) do
    down = move_down(briq)
    minz = min_max_z(briq) |> elem(0)

    disjoint = disjoint?(down, briqs)

    if disjoint and minz > 1 do
      insert(down, briqs)
    else
      {briq, [briq | briqs]}
    end
  end

  def disjoint?(_, []), do: true

  def disjoint?(briq, [b | rest]) do
    disjoint?(briq, b) and disjoint?(briq, rest)
  end

  def disjoint?({a, b, c}, {d, e, f}) do
    Range.disjoint?(a, d) or
      Range.disjoint?(b, e) or
      Range.disjoint?(c, f)
  end

  def move_down(b = {rx, ry, z0..z1}) do
    if z0 > 1, do: {rx, ry, (z0 - 1)..(z1 - 1)}, else: b
  end

  def min_max_z({_, _, z0..z1}), do: {z0, z1}

  def read() do
    File.stream!("data/day22.txt")
    |> Enum.map(fn line ->
      line
      |> String.trim()
      |> String.split("~")
      |> Enum.map(&String.split(&1, ","))
      |> Enum.zip()
      |> Enum.map(fn {s, e} -> String.to_integer(s)..String.to_integer(e) end)
    end)
    |> Enum.sort_by(fn [_x, _y, z0.._z1] -> z0 end)
    |> Enum.map(fn [x, y, z] -> {x, y, z} end)
  end
end
