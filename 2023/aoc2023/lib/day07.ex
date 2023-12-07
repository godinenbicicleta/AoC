defmodule Day07 do
  def p1, do: run(&mapper1/1)

  def p2, do: run(&mapper2/1)

  def run(mapper_func) do
    File.stream!("data/day07.txt")
    |> Enum.map(fn line ->
      line
      |> String.trim()
      |> String.split()
    end)
    |> Enum.map(fn [x, y] -> {x, String.to_integer(y)} end)
    |> Enum.sort_by(mapper_func)
    |> Enum.with_index(1)
    |> Enum.reduce(0, fn {{_, s}, rank}, acc -> rank * s + acc end)
  end

  def string_to_type(s) do
    freqs =
      s
      |> String.split("", trim: true)
      |> Enum.frequencies()
      |> Map.values()

    cond do
      5 in freqs -> 6
      4 in freqs -> 5
      3 in freqs and 2 in freqs -> 4
      3 in freqs and 2 not in freqs -> 3
      Enum.count(freqs, &(&1 == 2)) == 2 -> 2
      2 in freqs -> 1
      true -> 0
    end
  end

  def string_to_type2(s) do
    "AKQT98765432"
    |> String.split("", trim: true)
    |> Enum.map(&String.replace(s, "J", &1))
    |> Enum.map(&string_to_type/1)
    |> Enum.max()
  end

  def cards_to_order(s, to_score_func) do
    s
    |> String.split("", trim: true)
    |> Enum.map(to_score_func)
  end

  def to_score(s, order) do
    order
    |> String.split("", trim: true)
    |> Enum.with_index()
    |> Enum.into(%{})
    |> Map.get(s)
  end

  def to_score1(s), do: to_score(s, "23456789TJQKA")

  def to_score2(s), do: to_score(s, "J23456789TQKA")

  def mapper(s, convert_func, score_func) do
    type = convert_func.(s)
    cards = cards_to_order(s, score_func)
    {type, cards}
  end

  def mapper1({s, _}), do: mapper(s, &string_to_type/1, &to_score1/1)

  def mapper2({s, _}), do: mapper(s, &string_to_type2/1, &to_score2/1)
end
