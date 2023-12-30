defmodule Day25 do
  def main do
    rows = read()

    g =
      Enum.reduce(rows, %{}, fn [key, vals], map ->
        vals = String.split(vals)
        map = Map.update(map, key, vals, fn prev -> vals ++ prev end)

        Enum.reduce(vals, map, fn v, map ->
          Map.update(map, v, [key], fn prev -> [key | prev] end)
        end)
      end)

    runkey(g, key)
  end

  def runkey(g, key) do
    Enum.map(g[key],fn v -> runv(g, key, v) end
  end

  def runv(g, left, right) do

  end

  def get_edges(g) do
    Enum.map(g, fn {k, vs} ->
      Enum.zip(Stream.cycle([k]), vs)
      |> Enum.map(fn {x, y} ->
        [x, y]
        |> Enum.sort()
      end)
    end)
    |> Enum.concat()
    |> Enum.uniq()
  end

  def remove_edge(g, left, right) do
    Enum.map(g, fn {k, v} ->
      cond do
        k == left -> {k, v -- [right]}
        k == right -> {k, v -- [left]}
        true -> {k, v}
      end
    end)
    |> Enum.into(%{})
  end

  def run([], _g, seen), do: seen

  def run([current | queue], g, seen) do
    next = Map.get(g, current) |> Enum.filter(fn n -> not MapSet.member?(seen, n) end)

    seen = Enum.reduce(next, seen, fn n, seen -> MapSet.put(seen, n) end)
    run(next ++ queue, g, seen)
  end

  def read() do
    File.stream!("data/day25_test.txt")
    |> Enum.map(fn line ->
      line
      |> String.trim()
      |> String.split(": ")
    end)
  end
end
