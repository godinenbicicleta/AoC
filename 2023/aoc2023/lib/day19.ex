defmodule Day19 do
  def main do
    p1()
    p2()
  end

  def p2 do
    {workflows, _rankings} = read()

    {true, paths} =
      solve(workflows, "in")

    paths
    |> Enum.map(fn path -> Enum.group_by(path, &elem(&1, 0), fn {_, a, b} -> {a, b} end) end)
    |> Enum.map(fn line ->
      Enum.map(["a", "m", "x", "s"], fn label ->
        Enum.reduce(line[label] || [], 1..4000, fn {op, num}, r ->
          Enum.filter(r, fn x -> apply(Kernel, op, [x, num]) end)
        end)
        |> Enum.count()
      end)
      |> Enum.product()
    end)
    |> Enum.sum()
  end

  def solve(workflows, label) do
    rules = workflows[label]
    follow(rules, workflows)
  end

  def follow("A", _workflows), do: {true, [[]]}
  def follow(["A"], _workflows), do: {true, [[]]}
  def follow("R", _), do: {false, nil}
  def follow(["R"], _), do: {false, nil}

  def follow(label, workflows) when is_binary(label),
    do: follow(workflows[label], workflows)

  def follow([label], workflows) when is_binary(label),
    do: follow(workflows[label], workflows)

  def follow([{name, op, cond, dest} | rest], workflows) do
    {success, paths} = follow(rest, workflows)

    if_false =
      if success do
        {true, Enum.map(paths, fn p -> [{name, flip(op), cond} | p] end)}
      else
        {false, nil}
      end

    if_true =
      cond do
        dest == "A" ->
          {true, [[{name, op, cond}]]}

        dest == "R" ->
          {false, nil}

        true ->
          {success, paths} = follow(workflows[dest], workflows)

          if success do
            {true, Enum.map(paths, fn p -> [{name, op, cond} | p] end)}
          else
            {false, nil}
          end
      end

    case [if_true, if_false] do
      [{true, p1}, {true, p2}] -> {true, p1 ++ p2}
      [{true, p1}, {false, _}] -> {true, p1}
      [{false, _}, {true, p2}] -> {true, p2}
      _ -> {false, nil}
    end
  end

  def flip(:<), do: :>=
  def flip(:>), do: :<=

  def p1 do
    {workflows, rankings} = read()

    Enum.reduce(rankings, 0, fn ranking, acc ->
      case run(ranking, workflows, "in") do
        {1, 0} -> acc + (Map.values(ranking) |> Enum.sum())
        _ -> acc
      end
    end)
  end

  def run(_ranking, _workflows, "A"), do: {1, 0}
  def run(_ranking, _workflows, "R"), do: {0, 1}

  def run(ranking, workflows, label) do
    rules = workflows[label]

    Enum.reduce_while(rules, nil, fn rule, _acc ->
      cond do
        rule == "A" ->
          {:halt, {1, 0}}

        rule == "R" ->
          {:halt, {0, 1}}

        is_binary(rule) ->
          {:halt, run(ranking, workflows, rule)}

        true ->
          {name, op, num, dest} = rule

          if apply(Kernel, op, [ranking[name], num]) do
            {:halt, run(ranking, workflows, dest)}
          else
            {:cont, nil}
          end
      end
    end)
  end

  def read() do
    [workflows, rankings] =
      File.read!("data/day19.txt")
      |> String.trim()
      |> String.split("\n\n")

    workflows =
      workflows
      |> String.split("\n")
      |> Enum.map(fn line ->
        [name, rules] = String.split(line, "{")

        rules =
          String.split(rules, "}")
          |> hd
          |> String.split(",")
          |> Enum.map(&parse/1)

        {name, rules}
      end)
      |> Enum.into(%{})

    rankings =
      rankings
      |> String.split("\n")
      |> Enum.map(fn line ->
        line
        |> String.replace("{", "")
        |> String.replace("}", "")
        |> String.split(",")
        |> Enum.map(fn s ->
          [name, num] = String.split(s, "=")
          {name, String.to_integer(num)}
        end)
        |> Enum.into(%{})
      end)

    {workflows, rankings}
  end

  def parse(rule) do
    if String.contains?(rule, ":") do
      [condition, dest] = String.split(rule, ":")
      op = if String.contains?(condition, "<"), do: :<, else: :>
      [label, num] = String.split(condition, ["<", ">"])
      {label, op, String.to_integer(num), dest}
    else
      rule
    end
  end
end
