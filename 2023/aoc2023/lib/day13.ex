defmodule Day13 do
  def main do
    squares = get_squares()

    squares
    |> Enum.map(fn s ->
      [
        find(s),
        find(rotate(s), 0, 100)
      ]
    end)
    |> solve
    |> IO.inspect()

    # squares
    squares
    |> Enum.map(fn s ->
      [
        find(s),
        find(rotate(s), 0, 100),
        find(s, 1),
        find(rotate(s), 1, 100)
      ]
    end)
    |> solve
    |> IO.inspect()
  end

  def solve(s) do
    s
    |> Enum.map(fn x ->
      x
      |> Enum.concat()
      |> Enum.frequencies()
      |> Enum.min_by(&elem(&1, 1))
      |> elem(0)
      |> elem(0)
    end)
    |> Enum.sum()
  end

  def print_square(square) do
    square
    |> Enum.join("\n")
    |> IO.puts()
  end

  def get_squares() do
    File.read!("data/day13.txt")
    |> String.trim()
    |> String.split("\n\n")
    |> Enum.map(&String.split(&1, "\n"))
  end

  def find(square, offset \\ 0, times \\ 1) do
    size = length(square)

    Enum.reduce(square, [], fn row, square_set ->
      Enum.reduce(1..(byte_size(row) - 1), square_set, fn ix, set ->
        {left, right} = String.split_at(row, ix)
        left = left |> String.reverse() |> String.codepoints()
        right = right |> String.codepoints()

        if Enum.all?(Enum.zip(left, right), fn {l, r} -> l == r end),
          do: [ix | set],
          else: set
      end)
    end)
    |> Enum.frequencies()
    |> Enum.filter(fn {_x, y} -> y >= size - offset end)
    |> Enum.map(fn {x, y} -> {times * x, y} end)
  end

  def rotate(square) do
    map =
      square
      |> Enum.map(&String.codepoints/1)
      |> Enum.with_index()
      |> Enum.map(fn {s, i} -> {Enum.with_index(s), i} end)
      |> Enum.map(fn {row, y} -> Enum.map(row, fn {v, x} -> {{x, y}, v} end) end)
      |> List.flatten()
      |> Enum.into(%{})

    maxx = Enum.max_by(map, fn {{x, _}, _v} -> x end) |> elem(0) |> elem(0)
    maxy = Enum.max_by(map, fn {{_x, y}, _v} -> y end) |> elem(0) |> elem(1)

    Enum.reduce(0..maxx, [], fn x, acc ->
      [
        Enum.reduce(maxy..0, [], fn y, acc2 ->
          [map[{x, y}] | acc2]
        end)
        |> Enum.join()
        | acc
      ]
    end)
  end
end
