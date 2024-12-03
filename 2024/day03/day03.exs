defmodule Day03 do
  @mul_re ~r/mul\((?<x>\d+),(?<y>\d+)\)/
  @extract_re ~r/mul\(\d{1,3},\d{1,3}\)/
  @do_dont_re ~r/mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)/

  def run do
    File.stream!("input.txt")
    |> Enum.flat_map(&extract(&1, @extract_re))
    |> Enum.map(&mult/1)
    |> Enum.sum()
    |> IO.inspect(label: "p1")

    File.stream!("input.txt")
    |> Enum.flat_map(&extract(&1, @do_dont_re))
    |> Enum.reduce(
      {0, true},
      fn
        "do()", {total, _} ->
          {total, true}

        "don't()", {total, _} ->
          {total, false}

        _, {total, false} ->
          {total, false}

        elem, {total, true} ->
          [_, x, y] = Regex.run(@mul_re, elem)
          res = String.to_integer(x) * String.to_integer(y)
          {total + res, true}
      end
    )
    |> elem(0)
    |> IO.inspect(label: "p2")
  end

  def mult(s) do
    [_, x, y] = Regex.run(@mul_re, s)
    String.to_integer(x) * String.to_integer(y)
  end

  def extract(s, re) do
    Regex.scan(re, s)
    |> List.flatten()
  end
end
