defmodule Day1 do
  def run() do
    contents = File.read!("day1.txt")

    numset =
      Regex.scan(~r<\d+>, contents)
      |> Stream.map(&String.to_integer(hd(&1)))
      |> MapSet.new()

    Enum.reduce_while(numset, numset, &reducer/2)
    |> IO.inspect()

    Enum.reduce_while(numset, numset, &reducer2/2)
    |> IO.inspect()
  end

  def reducer(num, numset) do
    if MapSet.member?(numset, 2020 - num) do
      {:halt, num * (2020 - num)}
    else
      {:cont, numset}
    end
  end

  def reducer2(num, numset) do
    case Enum.find(numset, fn n -> MapSet.member?(numset, 2020 - num - n) end) do
      nil -> {:cont, numset}
      diff -> {:halt, num * (2020 - num - diff) * diff}
    end
  end
end

Day1.run()
