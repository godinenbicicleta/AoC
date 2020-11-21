defmodule Santa.String do
  def is_nice(string) do
    has_vowels(string) and twice(string) and not_forbidden(string)
  end

  def is_nice2(string) do
    has_pair?(string) and has_repeat(string)
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
