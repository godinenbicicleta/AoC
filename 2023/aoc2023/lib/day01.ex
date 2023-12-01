defmodule Day01 do
  @strs String.codepoints("123456789") ++
          ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
  @to_num %{
    "1" => 1,
    "2" => 2,
    "3" => 3,
    "4" => 4,
    "5" => 5,
    "6" => 6,
    "7" => 7,
    "8" => 8,
    "9" => 9,
    "one" => 1,
    "two" => 2,
    "three" => 3,
    "four" => 4,
    "five" => 5,
    "six" => 6,
    "seven" => 7,
    "eight" => 8,
    "nine" => 9
  }
  def p1() do
    File.stream!("data/day01.txt")
    |> Enum.map(&String.trim/1)
    |> solve
  end

  def solve(lines) do
    lines
    |> Enum.map(&String.split(&1, "", trim: true))
    |> Enum.map(&get_nums/1)
    |> Enum.reduce(0, fn {a, b}, acc -> 10 * a + b + acc end)
  end

  def p2() do
    File.stream!("data/day01.txt")
    |> Enum.map(&String.trim/1)
    |> Enum.map(fn line -> {find_first(line), find_last(line)} end)
    |> Enum.reduce(0, fn {a, b}, acc -> 10 * a + b + acc end)
  end

  def find_first(line) do
    res = Enum.find(@strs, fn s -> String.starts_with?(line, s) end)

    if res do
      @to_num[res]
    else
      find_first(String.slice(line, 1, String.length(line)))
    end
  end

  def find_last(line) do
    res = Enum.find(@strs, fn s -> String.ends_with?(line, s) end)

    if res do
      @to_num[res]
    else
      find_last(String.slice(line, 0, String.length(line) - 1))
    end
  end

  def p2test() do
    File.stream!("data/day01_test.txt")
    |> Enum.map(&String.trim/1)
  end

  def is_num(s) do
    Integer.parse(s) != :error
  end

  def get_nums(s) do
    rev = Enum.reverse(s)
    {n1, _x} = Enum.find(s, &is_num/1) |> Integer.parse()
    {n2, _x} = Enum.find(rev, &is_num/1) |> Integer.parse()
    {n1, n2}
  end
end
