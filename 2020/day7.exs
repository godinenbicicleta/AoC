defmodule Day7 do
  def read(file) do
    file
    |> File.stream!()
    |> Enum.into(%{}, &parse/1)
  end

  def run(bag_map, label, :p1) do
    {res, _, _} =
      bag_map
      |> Map.keys()
      |> Enum.reduce({0, MapSet.new(), MapSet.new()}, &reducer(&1, &2, label, bag_map))

    res - 1
  end

  def run(bag_map, label, :p2) do
    sum(bag_map, label, 0)
  end

  def sum(map, label, total) when is_map(map) do
    case Map.get(map, label) do
      nil -> 0
      map_vals -> sum(Map.to_list(map_vals), total, map)
    end
  end

  def sum([], total, _map), do: total

  def sum([{bag, num} | t], total, map) do
    sum(t, total + num + num * sum(map, bag, 0), map)
  end

  def contains(target, target, _map), do: true

  def contains(label, target, map) do
    case Map.get(map, label) do
      nil -> false
      values_map -> stack_contains(Map.keys(values_map), target, map)
    end
  end

  def stack_contains([target | _t], target, _map), do: true
  def stack_contains([], _, _), do: false

  def stack_contains([key | t], target, map) do
    case Map.get(map, key) do
      nil -> stack_contains(t, target, map)
      values_map -> stack_contains(Map.keys(values_map) ++ t, target, map)
    end
  end

  def reducer(key, {acc, cache_true, cache_false}, label, map) do
    case {MapSet.member?(cache_true, key), MapSet.member?(cache_false, key)} do
      {true, _} ->
        {acc + 1, cache_true, cache_false}

      {_, true} ->
        {acc, cache_true, cache_false}

      _ ->
        if contains(key, label, map) do
          {acc + 1, MapSet.put(cache_true, key), cache_false}
        else
          {acc, cache_true, MapSet.put(cache_false, key)}
        end
    end
  end

  @container ~r/(?<container>[\w ]+) bags contain (?<contained>.*).$/U
  @contained ~r/ ?(?<contents>[\d \w]+) bags?[\., ]?/
  def parse(line) do
    trimmed_line =
      line
      |> String.trim()

    %{"container" => container, "contained" => contained} =
      Regex.named_captures(@container, trimmed_line)

    contents =
      Regex.scan(@contained, contained)
      |> Enum.map(&Enum.at(&1, 1))

    if contents == ["no other"] do
      {container, nil}
    else
      {container, Enum.into(contents, %{}, &parse_contained/1)}
    end
  end

  def parse_contained(spec) do
    [num, label] = String.split(spec, " ", parts: 2)
    {label, String.to_integer(num)}
  end
end

Day7.read("day7.txt")
|> Day7.run("shiny gold", :p1)
|> IO.inspect()

Day7.read("day7.txt")
|> Day7.run("shiny gold", :p2)
|> IO.inspect()
