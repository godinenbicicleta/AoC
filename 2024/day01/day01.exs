defmodule Day01 do
  def run() do
    {d1, d2} =
      File.stream!("input.txt")
      |> Stream.map(&String.split/1)
      |> Stream.map(fn [x, y] -> {String.to_integer(x), String.to_integer(y)} end)
      |> Enum.unzip()

    d1 = Enum.sort(d1)
    d2 = Enum.sort(d2)

    Enum.zip_reduce(d1, d2, 0, fn x, y, acc -> abs(x - y) + acc end)
    |> IO.inspect(label: "p1")

    Enum.frequencies(d2)
    |> Stream.filter(fn {x, _} -> Enum.member?(d1, x) end)
    |> Enum.reduce(0, fn {x, y}, acc -> x * y + acc end)
    |> IO.inspect(label: "p2")
  end
end
