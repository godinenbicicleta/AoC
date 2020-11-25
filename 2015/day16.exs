defmodule Sue do
  @rules %{
    children: 3,
    cats: 7,
    samoyeds: 2,
    pomeranians: 3,
    akitas: 0,
    vizslas: 0,
    goldfish: 5,
    trees: 3,
    cars: 2,
    perfumes: 1
  }

  def solve() do
    File.read!("day16.txt")
    |> parse
    |> Enum.filter(fn {_sue, vals} -> filter(vals) end)
  end

  def solve2() do
    File.read!("day16.txt")
    |> parse
    |> Enum.filter(fn {_sue, vals} -> filter2(vals) end)
  end

  def filter(vals) do
    Enum.map(vals, fn {val, num} -> @rules[val] == num end)
    |> Enum.all?()
  end

  def filter2(vals) do
    Enum.map(vals, fn {val, num} -> apply_rule(val, num) end)
    |> Enum.all?()
  end

  def apply_rule(val, num) when val == :cats or val == :trees do
    comp = @rules[val]
    num > comp
  end

  def apply_rule(val, num) when val == :goldfish or val == :pomeranians do
    comp = @rules[val]
    num < comp
  end

  def apply_rule(val, num) do
    comp = @rules[val]
    num == comp
  end

  def parse(string) do
    string
    |> String.trim()
    |> String.split("\n", trim: true)
    |> Enum.into(%{}, &regex_parse/1)
  end

  def regex_parse(string) do
    [_, sue] = Regex.run(~r/Sue (\d+):/, string)
    sue = String.to_integer(sue)
    map = %{}

    map = add(string, map, :cats)
    map = add(string, map, :children)
    map = add(string, map, :samoyeds)
    map = add(string, map, :pomeranians)
    map = add(string, map, :akitas)
    map = add(string, map, :vizslas)
    map = add(string, map, :goldfish)
    map = add(string, map, :trees)
    map = add(string, map, :cars)
    map = add(string, map, :perfumes)
    {sue, map}
  end

  @regex_map %{
    cats: ~r/cats: (\d+)/,
    children: ~r/children: (\d+)/,
    samoyeds: ~r/samoyeds: (\d+)/,
    pomeranians: ~r/pomeraninas: (\d+)/,
    akitas: ~r/akitas: (\d+)/,
    vizslas: ~r/vizslas: (\d+)/,
    goldfish: ~r/goldfish: (\d+)/,
    trees: ~r/trees: (\d+)/,
    cars: ~r/cars: (\d+)/,
    perfumes: ~r/perfumes: (\d+)/
  }

  def add(string, map, key) do
    case Regex.run(@regex_map[key], string) do
      [_, x] -> Map.put(map, key, String.to_integer(x))
      nil -> map
    end
  end
end

Sue.solve()
|> IO.inspect()

Sue.solve2()
|> IO.inspect()
