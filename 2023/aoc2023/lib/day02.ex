defmodule Day02 do
  def p1() do
    File.stream!("data/day02.txt")
    |> Enum.map(&parse/1)
    |> Enum.filter(&possible?/1)
    |> Enum.reduce(0, fn [{x, _} | _], acc -> acc + x end)
  end

  def p2() do
    File.stream!("data/day02.txt")
    |> Enum.map(&process/1)
    |> Enum.sum()
  end

  def process(x) do
    parse(x)
    |> min_set
    |> Map.values()
    |> Enum.product()
  end

  def min_set(arr) do
    Enum.reduce(arr, %{}, fn {_, m}, acc ->
      Map.merge(m, acc, fn _key, v1, v2 -> max(v1, v2) end)
    end)
  end

  def possible?(arr) when is_list(arr) do
    Enum.all?(arr, &possible?/1)
  end

  def possible?({_, map}) do
    [{"red", 12}, {"green", 13}, {"blue", 14}]
    |> Enum.reduce(true, fn {color, num}, acc ->
      acc and Map.get(map, color, 0) <= num
    end)
  end

  def parse(line) do
    %{"game_id" => game_id} = Regex.named_captures(~r/Game (?<game_id>\d+):/, line)
    gid = String.to_integer(game_id)
    [_, rest] = String.split(line, ": ")

    subsets =
      String.split(rest, "; ")
      |> Enum.map(&parse_subset/1)

    Enum.zip(Stream.cycle([gid]), subsets)
  end

  def parse_subset(line) do
    [~r/(?<blue>\d+)\s+blue/, ~r/(?<red>\d+)\s+red/, ~r/(?<green>\d+)\s+green/]
    |> Enum.reduce(%{}, fn r, acc ->
      Regex.named_captures(r, line)
      |> Kernel.||(%{})
      |> Enum.into(%{}, fn {k, v} -> {k, String.to_integer(v)} end)
      |> Map.merge(acc)
    end)
  end
end
