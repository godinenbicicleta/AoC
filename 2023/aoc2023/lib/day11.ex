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

    galaxies = get_galaxies(grid, 2)
    gi = galaxies |> Enum.with_index()

    p1 =
      for {g1, i1} <- gi, {g2, i2} <- gi, i2 > i1, reduce: 0 do
        acc ->
          acc + shortest(g1, g2)
      end

    IO.puts("p1: #{p1}")
    galaxies = get_galaxies(grid, 1_000_000)
    gi = galaxies |> Enum.with_index()

    p2 =
      for {g1, i1} <- gi, {g2, i2} <- gi, i2 > i1, reduce: 0 do
        acc ->
          acc + shortest(g1, g2)
      end

    IO.puts("p1: #{p2}")
  end

  def get_galaxies(grid, times) do
    times = times - 1

    galaxies =
      Enum.filter(grid, fn {_, v} -> v == "#" end)
      |> Enum.map(&elem(&1, 0))
      |> Enum.sort()

    galaxies =
      galaxies
      |> expandx(times)
      |> Enum.sort_by(&elem(&1, 1))

    expandy(galaxies, times)
    |> Enum.sort()
  end

  def shortest({x1, y1}, {x2, y2}) do
    abs(x2 - x1) + abs(y2 - y1)
  end

  def diffs(g) do
    g
    |> Enum.chunk_every(2, 1, :discard)
    |> Enum.map(fn [{x1, _y1}, {x2, _y2}] -> x2 - x1 - 1 end)
    |> Enum.reduce([0], fn diff, [a | acc] ->
      if diff <= 0 do
        [a, a | acc]
      else
        [diff, a | acc]
      end
    end)
    |> Enum.reverse()
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

  def dimensions(m) do
    maxx = Enum.max_by(m, fn {x, _y} -> x end) |> elem(0) |> elem(0)
    minx = Enum.min_by(m, fn {x, _y} -> x end) |> elem(0) |> elem(0)
    maxy = Enum.max_by(m, fn {_x, y} -> y end) |> elem(0) |> elem(1)
    miny = Enum.min_by(m, fn {_x, y} -> y end) |> elem(0) |> elem(1)

    %{minx: minx, maxx: maxx, miny: miny, maxy: maxy}
  end
end
