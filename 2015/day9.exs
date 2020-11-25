defmodule Short do
  def solve(file) do
    distances = get_distances(file)
    cities = get_cities(distances)
    from_to = get_from_to(distances, cities)
    {distances, from_to}

    Enum.map(cities, fn value ->
      get_paths(
        value,
        distances,
        from_to,
        0,
        MapSet.new([value]),
        Enum.to_list(MapSet.delete(cities, value)),
        [value]
      )
    end)
    |> List.flatten()
    |> Enum.sort_by(fn x -> elem(x, 1) end)
  end

  def get_paths(
        _starting,
        _distances,
        _from_to,
        distance_traveled,
        _cities_visited,
        [],
        path
      ) do
    {path, distance_traveled}
  end

  def get_paths(
        starting,
        distances,
        from_to,
        distance_traveled,
        cities_visited,
        cities_remaining,
        path
      ) do
    from_to[starting]
    |> Enum.reject(fn x -> MapSet.member?(cities_visited, x) end)
    |> Enum.map(fn value ->
      new_cities_visited = MapSet.put(cities_visited, value)
      new_distance = distance_traveled + distances[{starting, value}]
      new_remaining = Enum.to_list(MapSet.delete(MapSet.new(cities_remaining), value))

      get_paths(value, distances, from_to, new_distance, new_cities_visited, new_remaining, [
        value | path
      ])
    end)
  end

  def get_cities(distances) do
    Map.keys(distances) |> Enum.map(&elem(&1, 0)) |> MapSet.new()
  end

  def get_from_to(distances, cities) do
    Enum.reduce(cities, %{}, fn city, acc ->
      Map.put(acc, city, filter(cities, city, distances))
    end)
  end

  def filter(cities, city, distances) do
    MapSet.delete(cities, city) |> Enum.filter(fn c -> Map.get(distances, {c, city}) end)
  end

  def get_distances(file) do
    file
    |> File.read!()
    |> parse
  end

  def parse(string) do
    string
    |> String.trim()
    |> String.split("\n", trim: true)
    |> Enum.map(&parse_route/1)
    |> List.flatten()
    |> Enum.into(%{})
  end

  def parse_route(string) do
    captures = Regex.named_captures(~r/(?<from>\w+)\sto\s(?<to>\w+)\s=\s(?<distance>\d+)/, string)
    distance = String.to_integer(captures["distance"])

    [
      {{captures["from"], captures["to"]}, distance},
      {{captures["to"], captures["from"]}, distance}
    ]
  end
end

paths = Short.solve("day9.txt")
paths |> hd |> IO.inspect()
paths |> List.last() |> IO.inspect()
