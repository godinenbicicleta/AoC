defmodule Santa.String do
  def is_nice(string) do
    has_vowels(string) and twice(string) and not_forbidden(string)
  end

  def is_nice2(string) do
    has_pair?(string) and has_repeat?(string)
  end

  def has_repeat?(string) when is_binary(string) do
    string
    |> String.graphemes()
    |> has_repeat?()
  end

  def has_repeat?([a, _, a]) do
    true
  end

  def has_repeat?([a, _, a | _]) do
    true
  end

  def has_repeat?([_ | t]) do
    has_repeat?(t)
  end

  def has_repeat?(_) do
    false
  end

  def has_pair?(string) when is_binary(string) do
    string
    |> String.graphemes()
    |> has_pair?(MapSet.new())
  end

  def has_pair?([a, b, a, b | _], _) do
    true
  end

  def has_pair?([a, a, a, b | t], set) when a != b do
    set = MapSet.put(set, {a, a}) |> MapSet.put({a, b})
    has_pair?([b | t], set)
  end

  def has_pair?([a, a, a | t], set) do
    if MapSet.member?(set, {a, a}) do
      true
    else
      has_pair?([a | t], MapSet.put(set, {a, a}))
    end
  end

  def has_pair?([a, b | t], set) do
    if MapSet.member?(set, {a, b}) do
      true
    else
      has_pair?([b | t], MapSet.put(set, {a, b}))
    end
  end

  def has_pair?(_, _) do
    false
  end

  def has_vowels(string) do
    case Regex.scan(~r<(a|e|i|o|u)>, string) do
      [_, _, _ | _] -> true
      _ -> false
    end
  end

  def twice(string) do
    string
    |> String.graphemes()
    |> twice("")
  end

  def twice([prev | _t], prev) do
    true
  end

  def twice([h | h], _) do
    true
  end

  def twice([h | t], _) do
    twice(t, h)
  end

  def twice(_, _) do
    false
  end

  def not_forbidden(string) do
    case Regex.run(~r<(ab|cd|pq|xy)>, string) do
      nil -> true
      _ -> false
    end
  end
end

File.read!("day5.txt")
|> String.trim()
|> String.split("\n")
|> Enum.count(&Santa.String.is_nice/1)
|> IO.inspect()

File.read!("day5.txt")
|> String.trim()
|> String.split("\n")
|> Enum.count(&Santa.String.is_nice2/1)
|> IO.inspect()
