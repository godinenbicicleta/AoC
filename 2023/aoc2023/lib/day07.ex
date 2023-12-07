defmodule Day07 do
  def p1 do
    run(&mapper/1)
  end

  def p2 do
    run(&mapper2/1)
  end

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
    ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    |> Enum.map(fn rep -> String.replace(s, "J", rep) end)
    |> Enum.map(&string_to_type/1)
    |> Enum.max()
  end

  def cards_to_order(s, to_score_func) do
    s
    |> String.split("", trim: true)
    |> Enum.map(to_score_func)
  end

  def to_score(s) do
    case s do
      "A" -> 14
      "K" -> 13
      "Q" -> 12
      "J" -> 11
      "T" -> 10
      "9" -> 9
      "8" -> 8
      "7" -> 7
      "6" -> 6
      "5" -> 5
      "4" -> 4
      "3" -> 3
      "2" -> 2
    end
  end

  def to_score2(s) do
    case s do
      "A" -> 14
      "K" -> 13
      "Q" -> 12
      "T" -> 10
      "9" -> 9
      "8" -> 8
      "7" -> 7
      "6" -> 6
      "5" -> 5
      "4" -> 4
      "3" -> 3
      "2" -> 2
      "J" -> 0
    end
  end

  def mapper({s, _}) do
    type = string_to_type(s)
    cards = cards_to_order(s, &to_score/1)
    {type, cards}
  end

  def mapper2({s, _}) do
    type = string_to_type2(s)
    cards = cards_to_order(s, &to_score2/1)
    {type, cards}
  end
end
