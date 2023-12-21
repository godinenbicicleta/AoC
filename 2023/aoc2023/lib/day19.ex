defmodule Day19 do
  def main do
    p1() |> IO.inspect()
    p2() |> IO.inspect()
  end

  def p2 do
    {workflows, _rankings} = read()

    solve(workflows, "in")
    |> Enum.map(fn path -> Enum.group_by(path, &elem(&1, 0), fn {_, a, b} -> {a, b} end) end)
    |> Enum.reduce(0, fn line, acc ->
      Enum.reduce(["a", "m", "x", "s"], 1, fn label, p ->
        Enum.reduce(line[label] || [], 1..4000, fn {op, num}, rstart..rend ->
          case op do
            :< -> rstart..min(rend, num - 1)
            :<= -> rstart..min(rend, num)
            :> -> max(rstart, num + 1)..rend
            :>= -> max(rstart, num)..rend
          end
        end)
        |> Range.size()
        |> Kernel.*(p)
      end)
      |> Kernel.+(acc)
    end)
  end

  def solve(workflows, label) do
    rules = workflows[label]
    follow(rules, workflows)
  end

  def follow("A", _workflows), do: [[]]
  def follow(["A"], _workflows), do: [[]]
  def follow("R", _), do: []
  def follow(["R"], _), do: []
  def follow(label, ws) when is_binary(label), do: follow(ws[label], ws)
  def follow([label], ws) when is_binary(label), do: follow(ws[label], ws)

  def follow([{name, op, cond, dest} | rest], ws) do
    if_false =
      follow(rest, ws)
      |> Enum.map(fn p -> [{name, flip(op), cond} | p] end)

    if_true =
      follow(ws[dest] || dest, ws)
      |> Enum.map(fn p -> [{name, op, cond} | p] end)

    if_true ++ if_false
  end

  def flip(:<), do: :>=
  def flip(:>), do: :<=

  def p1 do
    {workflows, rankings} = read()

    Enum.reduce(rankings, 0, fn ranking, acc ->
      if run(ranking, workflows, "in") do
        Enum.reduce(ranking, acc, fn {_, v}, acc -> acc + v end)
      else
        acc
      end
    end)
  end

  def run(_ranking, _workflows, "A"), do: true
  def run(_ranking, _workflows, "R"), do: false

  def run(ranking, workflows, label) do
    rules = workflows[label]

    Enum.reduce_while(rules, nil, fn rule, _acc ->
      cond do
        rule == "A" ->
          {:halt, true}

        rule == "R" ->
          {:halt, false}

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
