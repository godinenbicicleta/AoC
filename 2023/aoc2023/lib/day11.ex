defmodule Day11 do
  def main do
    grid =
      File.stream!("data/day11.txt")
      |> Enum.map(fn line ->
        line
        |> String.trim()
        |> String.codepoints()
        |> Enum.with_index()
      end)
      |> Enum.with_index()
      |> Enum.map(fn {row, y} -> Enum.map(row, fn {elem, x} -> {{x, y}, elem} end) end)
      |> List.flatten()
      |> Enum.into(%{})

    Enum.each(
      [2, 1_000_000],
      fn times ->
        galaxies = get_galaxies(grid, times - 1)
        gi = galaxies |> Enum.with_index()

        res =
          for {g1, i1} <- gi, {g2, i2} <- gi, i2 > i1, reduce: 0 do
            acc ->
              acc + shortest(g1, g2)
          end

        IO.puts("p#{times}: #{res}")
      end
    )
  end

  def get_galaxies(grid, times) do
    Enum.filter(grid, fn {_, v} -> v == "#" end)
    |> Enum.map(&elem(&1, 0))
    |> Enum.sort()
    |> expand(times, 0)
    |> Enum.sort_by(&elem(&1, 1))
    |> expand(times, 1)
    |> Enum.sort()
  end

  def shortest({x1, y1}, {x2, y2}) do
    abs(x2 - x1) + abs(y2 - y1)
  end

  def expand(galaxies, times, axis) do
    galaxies
    |> Enum.reduce({[], galaxies}, fn
      p, {[], original} ->
        {[p], original}

      p, {acc = [prev | _], [prev_original | rest]} ->
        old_diff = elem(p, axis) - elem(prev_original, axis)

        delta = max(old_diff - 1, 0) * times + old_diff

        new_elem = elem(prev, axis) + delta
        new_p = put_elem(p, axis, new_elem)

        {[new_p | acc], rest}
    end)
    |> elem(0)
    |> Enum.reverse()
  end
end
