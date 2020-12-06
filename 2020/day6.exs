defmodule Day6 do
  def run do
    File.read!("day6.txt")
    |> String.split("\n\n")
    |> Enum.reduce({0, 0}, &count/2)
  end

  def count(lines, {all, some}) do
    [union, intersection] =
      String.split(lines, "\n")
      |> Enum.map(&to_set/1)
      |> Enum.reduce({0, 0}, &reduce/2)
      |> Enum.map(&MapSet.size/1)

    {all + union, intersection + some}
  end

  def to_set(string) do
    string
    |> String.graphemes()
    |> MapSet.new()
  end

  def reduce(string_set, {0, 0}) do
    [string_set, string_set]
  end

  def reduce(string_set, [all, some]) do
    [MapSet.union(string_set, all), MapSet.intersection(string_set, some)]
  end
end
