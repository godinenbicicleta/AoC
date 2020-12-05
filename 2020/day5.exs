defmodule Day5 do
  def run do
    seats =
      File.stream!("day5.txt")
      |> Enum.into(MapSet.new(), &decode/1)

    # part 1
    {min, max} =
      Enum.min_max(seats)
      |> IO.inspect()

    all_ids = MapSet.new(min..max)

    # part 2
    MapSet.difference(all_ids, seats)
    |> IO.inspect()
  end

  def decode(string) do
    [row, column] = to_row_column(string)
    row * 8 + column
  end

  def to_row_column(string) do
    [{0..6, 0..127}, {7..9, 0..7}]
    |> Enum.map(fn {slice, range} -> get(String.slice(string, slice), range) end)
  end

  def get(string, range) do
    String.graphemes(string)
    |> Enum.reduce(range, &reduce/2)
    |> Enum.at(0)
  end

  def reduce(char, range = start..stop), do: reduce(char, range, div(start + stop, 2))
  def reduce("F", start..stop, mid), do: start..mid
  def reduce("L", start..stop, mid), do: start..mid
  def reduce("R", start..stop, mid), do: (mid + 1)..stop
  def reduce("B", start..stop, mid), do: (mid + 1)..stop
end
