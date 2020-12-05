defmodule Day4 do
  @re ~r/((\w{3}:[\w#]+) ?\n?)+/m
  @must_be ~w(byr iyr eyr hgt hcl ecl pid)
  @valid_eye MapSet.new(~w(amb blu brn gry grn hzl oth))
  @four_digit_re ~r<^\d{4}$>
  @hcl_re ~r/^#[0-9a-f]{6}$/
  @pid_re ~r/^\d{9}$/

  def run(part) do
    contents = File.read!("day4.txt")

    @re
    |> Regex.scan(contents)
    |> filter(part)
    |> length
  end

  def filter(parsed, :one) do
    Enum.filter(parsed, &contains_all?/1)
  end

  def filter(parsed, _) do
    Enum.filter(parsed, fn x -> contains_all?(x) and rules?(x) end)
  end

  def contains_all?([full_match | _]) do
    Enum.all?(@must_be, &String.contains?(full_match, &1))
  end

  def rules?([full_match | _]) do
    Regex.split(~r/\s/m, full_match, trim: true)
    |> Stream.map(&String.split(&1, ":"))
    |> Enum.all?(&valid?/1)
  end

  def valid?(["cid", _]), do: true
  def valid?(["byr", num]), do: valid_date?(num, 1920, 2002)
  def valid?(["iyr", num]), do: valid_date?(num, 2010, 2020)
  def valid?(["eyr", num]), do: valid_date?(num, 2020, 2030)
  def valid?(["hgt", num]), do: valid_height?(num)
  def valid?(["hcl", string]), do: valid_match?(@hcl_re, string)
  def valid?(["pid", num]), do: valid_match?(@pid_re, num)
  def valid?(["ecl", string]), do: MapSet.member?(@valid_eye, string)

  def valid_match?(re, string) do
    Regex.match?(re, string)
  end

  def cond_for(num, units, lower, upper) do
    without_suffix = String.trim_trailing(num, units)

    String.ends_with?(num, units) and
      valid_limits?(without_suffix, lower, upper)
  end

  def valid_height?(num) do
    cond do
      cond_for(num, "in", 59, 76) ->
        true

      cond_for(num, "cm", 150, 193) ->
        true

      true ->
        false
    end
  end

  def valid_limits?(num, lower, upper) do
    case Integer.parse(num) do
      {n, ""} -> n >= lower and n <= upper
      _ -> false
    end
  end

  def valid_date?(num, lower, upper) do
    Regex.match?(@four_digit_re, num) and valid_limits?(num, lower, upper)
  end
end

Day4.run(:one)
|> IO.inspect()

Day4.run(:two)
|> IO.inspect()
