defmodule Mole do
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

  def len([h | t_]) when is_list(h) do
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
