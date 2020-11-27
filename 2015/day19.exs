defmodule Mole do
  def solve2(file) do
    [rules_string, molecule] =
      File.read!(file)
      |> String.trim()
      |> String.split("\n\n", trim: true)

    rules = parse(rules_string)

    run(Enum.zip(Stream.cycle(["e"]), rules), rules, :cont, 0, molecule)
  end

  def run(_zip, _rules, :halt, steps, _molecule) do
    steps
  end

  def run(lz, rules, :cont, steps, molecule) do
    res =
      Stream.map(lz, fn {word, rule} ->
        mapply(rule, word)
      end)
      |> Stream.filter(fn x -> len(x) > 0 end)
      |> Enum.map(&join/1)
      |> List.flatten()
      |> Stream.filter(fn x -> String.length(x) <= String.length(molecule) end)
      |> Stream.uniq()
      |> Enum.map(fn x -> [x] end)

    if res == [] do
      run(nil, nil, :halt, steps, molecule)
    else
      unless Enum.any?(res, fn r -> r == molecule end) do
        m =
          Enum.map(res, fn r ->
            run(Enum.zip(Stream.cycle(r), rules), rules, :cont, steps + 1, molecule)
          end)
          |> List.flatten()
          |> Enum.uniq()

        m
      else
        run(nil, nil, :halt, steps, molecule)
      end
    end
  end

  def flat1(l = [h | t]) when is_list(h) do
    flat1(h) ++ flat1(t)
  end

  def flat1(x) do
    x
  end

  def solve() do
    [rules_string, molecule] =
      File.read!("day19.txt")
      |> String.trim()
      |> String.split("\n\n", trim: true)

    rules = parse(rules_string)

    res =
      Enum.map(rules, fn rule -> mapply(rule, molecule) end)
      |> Enum.filter(fn x -> len(x) > 0 end)
      |> Enum.map(&join/1)
      |> List.flatten()

    res =
      MapSet.new(res)
      |> MapSet.size()
  end

  def len([h | _t]) when is_list(h) do
    length(h)
  end

  def len(x) do
    length(x)
  end

  def join(x = [h | _]) when is_list(h) do
    Enum.map(x, fn y -> Enum.join(y, "") end)
  end

  def join(x) do
    Enum.join(x, "")
  end

  def mapply({string, subs}, molecule) do
    {:ok, re} = Regex.compile(string)
    splitted = String.split(molecule, re, include_captures: true, trim: true)
    num = length(Regex.scan(re, molecule))

    unless num == 0 do
      molecules = Stream.cycle([splitted]) |> Enum.take(num)
      replace(molecules, string, subs)
    else
      []
    end
  end

  def replace(molecules, string, subs) do
    molecule = hd(molecules)

    ixs =
      Enum.with_index(molecule)
      |> Enum.filter(fn {x, _} -> x == string end)
      |> Enum.map(fn {_, ix} -> ix end)

    Enum.zip(ixs, molecules)
    |> Enum.map(fn {ix, molecule} -> List.replace_at(molecule, ix, subs) end)
  end

  def parse(string) do
    string
    |> String.split("\n", trim: true)
    |> Enum.map(&reparse/1)
  end

  def reparse(string) do
    String.split(string, " => ")
    |> List.to_tuple()
  end
end
