defmodule Day2 do
  @re ~r<(\d+)-(\d+) (\w): (\w+)>
  def run() do
    contents = File.read!("day2.txt")

    parsed = Regex.scan(@re, contents)

    parsed
    |> Enum.reduce(0, &valid1/2)
    |> IO.inspect()

    parsed
    |> Enum.reduce(0, &valid2/2)
    |> IO.inspect()
  end

  def valid1([_, min, max, char, password], acc) do
    min = String.to_integer(min)
    max = String.to_integer(max)
    {:ok, re} = Regex.compile(char)
    len = length(Regex.scan(re, password))

    cond do
      len >= min and len <= max -> acc + 1
      true -> acc
    end
  end

  def valid2([_, one, two, char, password], acc) do
    one = String.to_integer(one) - 1
    two = String.to_integer(two) - 1
    charlist = String.to_charlist(password)
    [char_num] = String.to_charlist(char)

    case {Enum.at(charlist, one), Enum.at(charlist, two)} do
      {^char_num, ^char_num} -> acc
      {^char_num, _} -> acc + 1
      {_, ^char_num} -> acc + 1
      _ -> acc
    end
  end
end

Day2.run()
