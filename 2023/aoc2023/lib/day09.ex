defmodule Day09 do
  def p1 do
    File.stream!("data/day09.txt")
    |> Enum.map(fn line ->
      line
      |> String.trim()
      |> String.split()
      |> Enum.map(&String.to_integer/1)
    end)
    |> Enum.map(fn line ->
      line
      |> reduce()
      |> append(0)
      |> Enum.map(&List.last/1)
      |> List.last()
    end)
    |> Enum.sum()
  end

  def p2 do
    File.stream!("data/day09.txt")
    |> Enum.map(fn line ->
      line
      |> String.trim()
      |> String.split()
      |> Enum.map(&String.to_integer/1)
    end)
    |> Enum.map(fn line ->
      line
      |> reduce()
      |> prepend(0)
      |> List.last()
      |> hd
    end)
    |> Enum.sum()
  end

  def reduce(line) do
    Enum.reduce_while(line, [line], fn _, [row | rest] ->
      res =
        Enum.zip(tl(row), row)
        |> Enum.reduce([], fn {left, right}, acc -> [left - right | acc] end)
        |> Enum.reverse()

      if Enum.all?(Enum.map(res, &(&1 == 0))) do
        {:halt, [res, row | rest]}
      else
        {:cont, [res, row | rest]}
      end
    end)
  end

  def append([], _), do: []

  def append([line | lines], num) do
    reversed = Enum.reverse(line)
    [h | _] = reversed

    reversed =
      [h + num | reversed]
      |> Enum.reverse()

    [reversed | append(lines, h + num)]
  end

  def prepend([], _), do: []

  def prepend([line | lines], num) do
    [h | _] = line

    line = [h - num | line]

    [line | prepend(lines, h - num)]
  end
end
