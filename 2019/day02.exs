defmodule Day02 do
  def map_from_list(list) do
    Enum.zip(Stream.iterate(0, fn x -> x + 1 end), list)
    |> Enum.into(%{})
  end

  def update(codes, a, b) do
    codes = Map.put(codes, 1, a)
    Map.put(codes, 2, b)
  end

  def run(codes, pos) when is_map(codes) do
    code = Map.get(codes, pos)
    run(code, codes, pos)
  end

  def run(99, codes, _) do
    Map.get(codes, 0)
  end

  def run(1, codes, pos) do
    pos_num1 = Map.get(codes, pos + 1)
    pos_num2 = Map.get(codes, pos + 2)
    num1 = Map.get(codes, pos_num1)
    num2 = Map.get(codes, pos_num2)
    dest = Map.get(codes, pos + 3)
    codes = Map.put(codes, dest, num1 + num2)
    run(codes, pos + 4)
  end

  def run(2, codes, pos) do
    pos_num1 = Map.get(codes, pos + 1)
    pos_num2 = Map.get(codes, pos + 2)
    num1 = Map.get(codes, pos_num1)
    num2 = Map.get(codes, pos_num2)
    dest = Map.get(codes, pos + 3)
    codes = Map.put(codes, dest, num1 * num2)
    run(codes, pos + 4)
  end
end

[1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
|> Day02.map_from_list()
|> Day02.run(0)
|> IO.inspect()

[1, 0, 0, 0, 99]
|> Day02.map_from_list()
|> Day02.run(0)
|> IO.inspect()

[1, 1, 1, 4, 99, 5, 6, 0, 99]
|> Day02.map_from_list()
|> Day02.run(0)
|> IO.inspect()

File.read!("input02.txt")
|> String.trim()
|> String.split(",")
|> Enum.map(&String.to_integer/1)
|> Day02.map_from_list()
|> Day02.update(12, 2)
|> Day02.run(0)
|> IO.inspect()

nums =
  File.read!("input02.txt")
  |> String.trim()
  |> String.split(",")
  |> Enum.map(&String.to_integer/1)
  |> Day02.map_from_list()

try do
  for a <- 0..99, b <- 0..99 do
    res =
      Day02.update(nums, a, b)
      |> Day02.run(0)

    case res do
      19_690_720 ->
        (100 * a + b)
        |> IO.inspect()

        throw(:break)

      _ ->
        nil
    end
  end
catch
  :break -> nil
end
