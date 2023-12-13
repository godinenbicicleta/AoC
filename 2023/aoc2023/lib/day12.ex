defmodule Day12 do
  def main() do
    {p1, cache} = solve(1, %{})
    {p2, _} = solve(5, cache)

    {p1, p2}
  end

  def solve(times, cache) do
    File.stream!("data/day12.txt")
    |> Enum.map(fn line ->
      line
      |> String.trim()
      |> String.split()
    end)
    |> Enum.reduce({0, cache}, fn [springs, counts], {total, cache} ->
      counts =
        counts
        |> String.split(",")
        |> Enum.map(&String.to_integer/1)
        |> then(fn c -> Enum.map(1..times, fn _ -> c end) end)
        |> Enum.concat()

      springs =
        Enum.map(1..times, fn _ -> springs end)
        |> Enum.join("?")
        |> String.codepoints()

      {res, cache} = count_ways(springs, counts, cache)
      {total + res, cache}
    end)
  end

  def count_ways(s, counts, cache) do
    cached = Map.get(cache, {s, counts})

    {res, cache} =
      cond do
        cached != nil ->
          {cached, cache}

        counts == [] and "#" in s ->
          {0, cache}

        counts == [] ->
          {1, cache}

        s != [] and hd(s) == "." ->
          count_ways(tl(s), counts, cache)

        length(s) < hd(counts) ->
          {0, cache}

        hd(s) == "#" and Enum.take_while(s, &(&1 == "#")) |> Enum.count() > hd(counts) ->
          {0, cache}

        true ->
          count_with_prefix(s, counts, cache)
      end

    {res, Map.put_new(cache, {s, counts}, res)}
  end

  def count_with_prefix(s, counts, cache) do
    prefix = Enum.take(s, hd(counts))

    next = Enum.drop(s, hd(counts))
    rest = Enum.drop(s, hd(counts) + 1)

    res =
      cond do
        "." in prefix and hd(prefix) == "?" ->
          count_ways(tl(s), counts, cache)

        "." in prefix ->
          {0, cache}

        prefix == Stream.cycle(["#"]) |> Enum.take(hd(counts)) ->
          count_ways(rest, tl(counts), cache)

        next != [] and hd(next) == "#" and hd(prefix) == "#" ->
          {0, cache}

        next != [] and hd(next) == "#" and hd(prefix) != "#" ->
          count_ways(tl(s), counts, cache)

        hd(prefix) == "#" ->
          count_ways(rest, tl(counts), cache)

        true ->
          {left, cache} = count_ways(rest, tl(counts), cache)
          {right, cache} = count_ways(tl(s), counts, cache)
          {left + right, cache}
      end

    res
  end
end
