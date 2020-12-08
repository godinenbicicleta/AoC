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

  def run(ops, :one), do: run(ops, MapSet.new(), 0, 0)
  def run(ops, :two), do: run_with_flips(ops, 0)

  def run(ops, _seen, ix, acc) when not is_map_key(ops, ix), do: IO.puts(acc)

  def run(ops, seen, ix, acc) do
    if MapSet.member?(seen, ix) do
      IO.puts(acc)
      false
    else
      op = Map.get(ops, ix)

      case apply_op(op, ops, MapSet.put(seen, ix), ix, acc) do
        nil -> true
        val -> val
      end
    end
  end

  def run_with_flips(ops, flipix) do
    if run(Map.update!(ops, flipix, &updater/1), MapSet.new(), 0, 0) do
      nil
    else
      run_with_flips(ops, flipix + 1)
    end
  end

  def updater({"acc", _} = v), do: v
  def updater({"nop", num}), do: {"jmp", num}
  def updater({"jmp", num}), do: {"nop", num}

  def apply_op({"acc", num}, ops, seen, ix, acc), do: run(ops, seen, ix + 1, acc + num)
  def apply_op({"jmp", num}, ops, seen, ix, acc), do: run(ops, seen, ix + num, acc)
  def apply_op({"nop", _num}, ops, seen, ix, acc), do: run(ops, seen, ix + 1, acc)
end

Day8.read()
|> Day8.run(:one)
|> IO.inspect()

Day8.read()
|> Day8.run(:two)
|> IO.inspect()
