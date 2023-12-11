defmodule Day11 do
  def p1 do
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
        galaxies = get_galaxies(grid, times)
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
    times = times - 1

    Enum.filter(grid, fn {_, v} -> v == "#" end)
    |> Enum.map(&elem(&1, 0))
    |> Enum.sort()
    |> expandx(times)
    |> Enum.sort_by(&elem(&1, 1))
    |> expandy(times)
    |> Enum.sort()
  end

  def shortest({x1, y1}, {x2, y2}) do
    abs(x2 - x1) + abs(y2 - y1)
  end

  def expandx(galaxies, times) do
    galaxies
    |> Enum.reduce({[], galaxies}, fn
      p, {[], original} ->
        {[p], original}

      {x, y}, {acc = [prev | _], [prev_original | rest]} ->
        old_diff = x - elem(prev_original, 0)

        delta =
          if old_diff > 1 do
            (old_diff - 1) * times
          else
            0
          end

        new_elem = {elem(prev, 0) + delta + old_diff, y}

        {[new_elem | acc], rest}
    end)
    |> elem(0)
    |> Enum.reverse()
  end

  def expandy(galaxies, times) do
    galaxies
    |> Enum.reduce({[], galaxies}, fn
      p, {[], original} ->
        {[p], original}

      {x, y}, {acc = [prev | _], [prev_original | rest]} ->
        old_diff = y - elem(prev_original, 1)

        delta =
          if old_diff > 1 do
            (old_diff - 1) * times
          else
            0
          end

        new_elem = {x, elem(prev, 1) + old_diff + delta}

        {[new_elem | acc], rest}
    end)
    |> elem(0)
    |> Enum.reverse()
  end
end
