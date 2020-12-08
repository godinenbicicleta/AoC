defmodule Day8 do
  def read do
    File.stream!("day8.txt")
    |> Enum.with_index()
    |> Enum.into(%{}, &parse/1)
  end

  def parse({string, ix}) do
    [op, num] =
      string
      |> String.trim()
      |> String.split(" ")

    {ix, {op, String.to_integer(num)}}
  end

  def run(ops, :one) do
    seen = MapSet.new()
    ix = 0
    acc = 0
    run(ops, seen, ix, acc)
  end

  def run(ops, seen, ix, acc) do
    if MapSet.member?(seen, ix) do
      IO.puts(acc)
    else
      op = Map.get(ops, ix)
      apply_op(op, ops, MapSet.put(seen, ix), ix, acc)
    end
  end

  def apply_op({"acc", num}, ops, seen, ix, acc) do
    run(ops, seen, ix + 1, acc + num)
  end

  def apply_op({"jmp", num}, ops, seen, ix, acc) do
    run(ops, seen, ix + num, acc)
  end

  def apply_op({"nop", num}, ops, seen, ix, acc) do
    run(ops, seen, ix + 1, acc)
  end
end

Day8.read()
|> Day8.run(:one)
|> IO.inspect()
