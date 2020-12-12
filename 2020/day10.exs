defmodule Day10 do
  def run do
    nums =
      File.stream!("day10.txt")
      |> Enum.into(MapSet.new(), &parse/1)
      |> fill()

    sorted = Enum.sort(nums)

    # part 1
    Enum.zip(sorted, tl(sorted))
    |> Enum.map(fn {x, y} -> y - x end)
    |> Enum.frequencies()
    |> IO.inspect()
    |> Enum.reduce(1, &reducer/2)
    |> IO.inspect()

    # part 2
    sorted
    |> Stream.filter(&filter(&1, nums))
    |> Stream.chunk_while([], &chunker/2, &after_fun/1)
    |> Enum.reduce(1, &find_solutions(&1, &2, nums))
    |> IO.inspect()
  end

  def reducer({1, val}, acc), do: val * acc
  def reducer({3, val}, acc), do: val * acc
  def recucer(_, acc), do: acc

  def find_solutions(chunk, acc, data) when is_integer(acc) do
    acc * length(find_solutions(chunk, data, MapSet.new()))
  end

  def find_solutions([], _data, removed) do
    [removed]
  end

  def find_solutions([h | t], data, removed) do
    s = find_solutions(t, data, removed)

    if filter(h, data) do
      find_solutions(t, MapSet.delete(data, h), [h | removed]) ++ s
    else
      s
    end
  end

  def after_fun([]), do: {:cont, []}
  def after_fun(acc), do: {:cont, acc, []}

  def chunker(elem, []), do: {:cont, [elem]}
  def chunker(elem, acc = [h | _]) when elem - h <= 3, do: {:cont, [elem | acc]}
  def chunker(elem, acc), do: {:cont, acc, [elem]}

  def fill(nums) do
    max = Enum.max(nums)
    MapSet.union(nums, MapSet.new([0, max + 3]))
  end

  def filter(num, nums) do
    case {(num - 1) in nums, (num - 2) in nums, (num + 1) in nums, (num + 2) in nums} do
      {true, _, true, _} -> true
      {true, _, _, true} -> true
      {_, true, true, _} -> true
      _ -> false
    end
  end

  def parse(num) do
    num
    |> String.trim()
    |> String.to_integer()
  end
end
