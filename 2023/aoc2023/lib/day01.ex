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
    |> Enum.map(&String.codepoints/1)
    |> Enum.map(&get_nums/1)
    |> sum
  end

  def p2() do
    File.stream!("data/day01.txt")
    |> Enum.map(&String.trim/1)
    |> Enum.map(fn line -> {find_first(line), find_last(line)} end)
    |> sum
  end

  def sum(nums) do
    nums
    |> Enum.reduce(0, fn {a, b}, acc -> 10 * a + b + acc end)
  end

  def find_first(line) do
    res = Enum.find(@strs, fn s -> String.starts_with?(line, s) end)

    if res do
      @to_num[res]
    else
      find_first(String.slice(line, 1..-1))
    end
  end

  def find_last(line) do
    res = Enum.find(@strs, fn s -> String.ends_with?(line, s) end)

    if res do
      @to_num[res]
    else
      find_last(String.slice(line, 0..-2))
    end
  end

  def is_num?(s) do
    Integer.parse(s) != :error
  end

  def get_nums(s) do
    rev = Enum.reverse(s)
    {n1, _} = Enum.find(s, &is_num?/1) |> Integer.parse()
    {n2, _} = Enum.find(rev, &is_num?/1) |> Integer.parse()
    {n1, n2}
  end
end
