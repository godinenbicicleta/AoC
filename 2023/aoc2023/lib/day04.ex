defmodule Day04 do
  def p1 do
    File.stream!("data/day04.txt")
    |> Enum.map(&process/1)
    |> Enum.map(&elem(&1, 1))
    |> Enum.filter(&(&1 > 0))
    |> Enum.map(fn x -> 2 ** (x - 1) end)
    |> Enum.sum()
  end

  def p2 do
    cards =
      File.stream!("data/day04.txt")
      |> Enum.map(&process/1)
      |> Enum.into(%{})

    Enum.reduce(cards, {map_size(cards), cards}, &reducer/2)
    |> elem(0)
  end

  def reducer({k, v}, acc = {total, cards}) do
    if v == 0 do
      acc
    else
      new_cards =
        Enum.filter(cards, fn {c, _} -> c - k >= 1 && c - k <= v end)
        |> Enum.into(%{})

      {t, _} = Enum.reduce(new_cards, {map_size(new_cards), cards}, &reducer/2)
      {total + t, cards}
    end
  end

  def process(line) do
    [card, nums] =
      line
      |> String.trim()
      |> String.split("|")

    [card_str, winners] = card |> String.split(":")

    [[_, id_str]] = Regex.scan(~r/Card\s+(\d+)/, card_str)

    winners =
      winners
      |> String.split(" ", trim: true)
      |> Enum.map(&String.to_integer/1)
      |> Enum.into(MapSet.new())

    nums =
      nums
      |> String.split(" ", trim: true)
      |> Enum.map(&String.to_integer/1)
      |> Enum.into(MapSet.new())

    winner_count =
      MapSet.intersection(winners, nums)
      |> Enum.count()

    {String.to_integer(id_str), winner_count}
  end
end
