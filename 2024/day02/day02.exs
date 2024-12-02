defmodule Day02 do
  def run do
    arr =
      File.stream!("input.txt")
      |> Enum.map(fn x ->
        arr =
          String.split(x)
          |> Enum.map(&String.to_integer/1)

        arr |> Enum.zip_with(Enum.drop(arr, 1), &(&2 - &1))
      end)

    arr
    |> Enum.filter(&safe1/1)
    |> Enum.count()
    |> IO.inspect(label: "p1")

    arr
    |> Enum.filter(&safe2/1)
    |> Enum.count()
    |> IO.inspect(label: "p2")
  end

  def safe1(arr) do
    all_increasing = Enum.all?(arr, &(&1 > 0))
    all_decreasing = Enum.all?(arr, &(&1 < 0))
    {min, max} = Enum.min_max(arr)

    (all_increasing && max <= 3) || (all_decreasing && min >= -3)
  end

  def safe2(arr) do
    safe1(arr) || safe2(arr, 0)
  end

  def safe2(arr, ix) do
    ix < length(arr) and (safe1(List.delete_at(arr, ix)) or safe2(arr, ix + 1))
  end
end
