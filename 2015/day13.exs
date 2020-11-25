defmodule Table do
  def read(file) do
    File.read!(file)
    |> String.trim()
    |> String.split("\n", trim: true)
  end

  def solve(file) do
    contents = file |> read
    sd = contents |> score_dict
    ns = sd |> names

    sdict = sd |> Enum.map(fn {x, y} -> {x, Enum.into(y, %{})} end) |> Enum.into(%{})

    ns
    |> perm
    |> flatten
    |> Enum.map(fn x -> x ++ [hd(x)] end)
    |> Enum.map(fn x -> Enum.zip(x, tl(x)) end)
    |> Enum.map(&add_total(&1, sdict))
    |> Enum.map(&Enum.sum/1)
    |> Enum.max()
  end

  def solve_me(file) do
    contents = file |> read
    sd = contents |> score_dict
    sd = update_sd(sd)
    ns = sd |> names

    sdict = sd |> Enum.map(fn {x, y} -> {x, Enum.into(y, %{})} end) |> Enum.into(%{})

    ns
    |> perm
    |> flatten
    |> Enum.map(fn x -> x ++ [hd(x)] end)
    |> Enum.map(fn x -> Enum.zip(x, tl(x)) end)
    |> Enum.map(&add_total(&1, sdict))
    |> Enum.map(&Enum.sum/1)
    |> Enum.max()
  end

  def update_sd(sd) do
    new = Enum.map(sd, fn {x, y} -> {x, [{"Bruno", 0} | y]} end) |> Enum.into(%{})
    bruno_list = Enum.map(sd, fn {x, _} -> {x, 0} end)
    Map.put(new, "Bruno", bruno_list)
  end

  def add_total(tuple_list, sd) do
    Enum.map(tuple_list, fn {a, b} -> sd[a][b] + sd[b][a] end)
  end

  def score_dict(contents) do
    Enum.reduce(contents, %{}, &parse/2)
  end

  def names(score_dict) do
    Map.keys(score_dict)
  end

  def perm([name]) do
    [name]
  end

  def perm(name) when is_binary(name) do
    [name]
  end

  def perm(name_list) do
    perm(name_list, [])
  end

  def perm([], done) do
    done
  end

  def perm(name_list, done) do
    for name <- name_list do
      remaining = Enum.reject(name_list, fn x -> x == name end)

      perm(remaining, [name | done])
    end
  end

  def flatten([]) do
    []
  end

  def flatten(list = [[smth | _] | _]) when is_binary(smth) do
    list
  end

  def flatten(list = [[smth | _] | tail]) when is_list(smth) do
    flatten(hd(list)) ++ flatten(tail)
  end

  @re ~r/(?<from>\w+) would (?<sign>lose|gain) (?<score>\d+).+ to (?<to>\w+)/
  def parse(string, acc) do
    %{"from" => from, "score" => score, "sign" => sign, "to" => to} =
      Regex.named_captures(@re, string)

    score = parse_score(score, sign)

    from_entry =
      case Map.get(acc, from) do
        nil -> []
        entry -> entry
      end

    acc
    |> Map.put(from, [{to, score} | from_entry])
  end

  def parse_score(score, "lose") do
    String.to_integer(score) * -1
  end

  def parse_score(score, "gain") do
    String.to_integer(score)
  end
end

Table.solve("day13.txt") |> IO.inspect()
Table.solve_me("day13.txt") |> IO.inspect()
