defmodule Day05 do
  @map_keys [
    :seed_to_soil,
    :soil_to_fertilizer,
    :fertilizer_to_water,
    :water_to_light,
    :light_to_temperature,
    :temperature_to_humidity,
    :humidity_to_location
  ]
  def p1 do
    {seeds, map} = parse("data/day05.txt")

    Enum.reduce(
      @map_keys,
      seeds,
      fn key, acc -> Enum.map(acc, &transform(&1, map, key)) end
    )
    |> Enum.min()
  end

  def p2 do
    {seeds, map} = parse("data/day05.txt")

    seeds
    |> Enum.chunk_every(2)
    |> Enum.map(fn [start, e] -> reducer(start, start + e - 1, map) end)
    |> Enum.min()
  end

  def reducer(start, end_point, map) do
    start_location = to_location(start, map)
    end_location = to_location(end_point, map)

    cond do
      end_point <= start ->
        start_location

      end_location - start_location == start - end_point ->
        start_location

      start_location - end_location == start - end_point ->
        end_location

      true ->
        mid = div(start + end_point, 2)
        left = reducer(start, mid, map)

        right = reducer(mid + 1, end_point, map)

        min(left, right)
    end
  end

  def to_location(seed, map) do
    Enum.reduce(@map_keys, seed, &transform(&2, map, &1))
  end

  def transform(seed, map, key) do
    Enum.reduce_while(map[key], seed, fn [dest, src, len], acc ->
      if acc in src..(src + len - 1) do
        {:halt, acc + (dest - src)}
      else
        {:cont, acc}
      end
    end)
  end

  def parse(fname) do
    lines =
      File.read!(fname)
      |> String.trim()
      |> String.split("\n\n")

    [seeds | rest] = lines

    vals = rest |> Enum.map(&parse_map/1)

    map =
      Enum.zip(@map_keys, vals)
      |> Map.new()

    seeds =
      seeds
      |> String.split()
      |> tl
      |> Enum.map(&String.to_integer/1)

    {seeds, map}
  end

  def parse_map(x) do
    x
    |> String.split("\n")
    |> tl
    |> Enum.map(fn x ->
      x
      |> String.split()
      |> Enum.map(&String.to_integer/1)
    end)
  end
end
