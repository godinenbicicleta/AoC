defmodule Wire do
  use Bitwise

  @re1 ~r/(?<operation>[\w\s]+) -> (?<result>\w+)/

  def read(file) do
    File.read!(file)
    |> parse()
    |> Enum.to_list()
  end

  def read2(file) do
    File.read!(file)
    |> parse()
    |> sub()
    |> Enum.to_list()
  end

  def sub(map) do
    Map.put(map, "b", 956)
  end

  def parse(contents) do
    contents
    |> String.trim()
    |> String.split("\n")
    |> Enum.reduce(%{}, &parse_ops/2)
  end

  def solve(file) do
    instructions = read(file)
    evaluate(instructions, %{})
  end

  def solve2(file) do
    instructions = read2(file)
    evaluate(instructions, %{})
  end

  def evaluate([], ev) do
    ev
  end

  def evaluate(instructions, evaluated) do
    {solved, unsolved} = Enum.split_with(instructions, fn {_, y} -> is_integer(y) end)
    evaluated = Enum.into(Enum.into(solved, %{}), evaluated)
    unsolved = Enum.map(unsolved, fn x -> replace(x, evaluated) end)
    evaluate(unsolved, evaluated)
  end

  def replace({key, {nil, nil, smth}}, evaluated) do
    case Map.get(evaluated, smth) do
      nil -> {key, {nil, nil, smth}}
      num -> {key, num}
    end
  end

  def replace({key, {op, smth, nil}}, evaluated) do
    case Map.get(evaluated, smth) do
      nil -> {key, {op, smth, nil}}
      num -> {key, apply(op, [num])}
    end
  end

  def replace({key, {op, l, r}}, evaluated) do
    case {is_integer(l), is_integer(r)} do
      {true, true} -> {key, apply(op, [l, r])}
      {false, true} -> {key, {op, Map.get(evaluated, l, l), r}}
      {true, false} -> {key, {op, l, Map.get(evaluated, r, r)}}
      {false, false} -> {key, {op, Map.get(evaluated, l, l), Map.get(evaluated, r, r)}}
    end
  end

  def parse_ops(string, acc) do
    %{"operation" => operation, "result" => result} = Regex.named_captures(@re1, string)

    op =
      operation
      |> String.split(" ")
      |> parse_op()

    Map.put(acc, result, op)
  end

  @operations %{
    "RSHIFT" => &Bitwise.bsr/2,
    "LSHIFT" => &Bitwise.bsl/2,
    "AND" => &Bitwise.&&&/2,
    "OR" => &Bitwise.|||/2
  }
  def parse_op([one, op, three]) do
    operation = Map.get(@operations, op)

    case {Integer.parse(one), Integer.parse(three)} do
      {{l, _}, {r, _}} -> apply(operation, [l, r])
      {:error, {r, _}} -> {operation, one, r}
      {{l, _}, :error} -> {operation, l, three}
      {:error, :error} -> {operation, one, three}
    end
  end

  def parse_op(["NOT", smth]) do
    case Integer.parse(smth) do
      {num, _} -> apply(&not_op/1, [num])
      :error -> {&not_op/1, smth, nil}
    end
  end

  def parse_op([smth]) do
    case Integer.parse(smth) do
      {num, _} -> num
      _ -> {nil, nil, smth}
    end
  end

  def not_op(num) do
    Bitwise.bnot(num) + 65536
  end
end

Wire.solve("day7.txt")["a"]
|> IO.inspect()

Wire.solve2("day7.txt")["a"]
|> IO.inspect()
