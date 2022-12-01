defmodule Main do
  @pattern ~r/#(?<id>\d+)\s@\s(?<x>\d+),(?<y>\d+):\s(?<w>\d+)x(?<h>\d+)\s?/
  def parse(s),
    do:
      Regex.named_captures(@pattern, s)
      |> Enum.map(fn {key, v} -> {key, String.to_integer(v)} end)
      |> Map.new()

  def reduce(elem, acc) do
    {rx, ry} = to_range(elem)

    for x <- rx, y <- ry, reduce: acc do
      acc -> Map.update(acc, {x, y}, [elem["id"]], &[elem["id"] | &1])
    end
  end

  def to_range(elem) do
    minx = elem["x"]
    maxx = elem["x"] + elem["w"] - 1
    miny = elem["y"]
    maxy = elem["y"] + elem["h"] - 1
    {minx..maxx, miny..maxy}
  end

  def to_points(elem) do
    {elemx, elemy} = to_range(elem)
    acc = MapSet.new()

    for x <- elemx, y <- elemy, reduce: acc do
      acc -> MapSet.put(acc, {x, y})
    end
  end

  def matches({elem, points}, all_points) do
    elems = Enum.filter(all_points, fn {e, _} -> e["id"] != elem["id"] end)

    Enum.all?(elems, fn {_, ps} ->
      MapSet.disjoint?(ps, points)
    end)
  end

  def run() do
    parsed =
      File.stream!("input.txt")
      |> Enum.map(&parse/1)

    Enum.reduce(parsed, %{}, &reduce/2)
    |> Enum.filter(&(length(elem(&1, 1)) > 1))
    |> length
    |> IO.inspect()

    points = Enum.map(parsed, &{&1, to_points(&1)})

    Enum.filter(points, &matches(&1, points))
    |> hd
    |> elem(0)
    |> IO.inspect()
  end
end
