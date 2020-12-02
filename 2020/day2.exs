defmodule Day2 do
  @re ~r<(\d+)-(\d+) (\w): (\w+)>
  def run() do
    contents = File.read!("day2.txt")

    parsed =
      Regex.scan(@re, contents)
      |> Enum.map(&parse_ints/1)

    parsed
    |> Enum.reduce(0, &count_valids(&1, &2, :p1))
    |> IO.inspect()

    parsed
    |> Enum.reduce(0, &count_valids(&1, &2, :p2))
    |> IO.inspect()
  end

  def parse_ints([_, min, max, char, password]) do
    {min, max} = {String.to_integer(min), String.to_integer(max)}
    [min, max, char, password]
  end

  def count_valids([min, max, char, password], acc, part) do
    if valid?([min, max, char, password], part) do
      acc + 1
    else
      acc
    end
  end

  def valid?([min, max, char, password], :p1) do
    {:ok, re} = Regex.compile(char)
    len = length(Regex.scan(re, password))

    if len >= min and len <= max do
      true
    else
      false
    end
  end

  def valid?([one, two, char, password], :p2) do
    first = one - 1
    second = two - 1
    slices = {String.slice(password, first, 1), String.slice(password, second, 1)}

    case slices do
      {^char, ^char} -> false
      {^char, _} -> true
      {_, ^char} -> true
      _ -> false
    end
  end
end

Day2.run()
