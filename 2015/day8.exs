defmodule Space do
  def compute(content) do
    one =
      content
      |> String.trim()
      |> String.split("\n", trim: true)
      |> Enum.map(&String.trim(&1, "\""))
      |> Enum.map(&clean/1)
      |> Enum.map(&String.length/1)
      |> Enum.sum()

    two =
      content
      |> String.trim()
      |> String.split("\n", trim: true)
      |> Enum.map(&String.length/1)
      |> Enum.sum()

    three =
      content
      |> String.trim()
      |> String.split("\n", trim: true)
      |> Enum.map(&unclean/1)
      |> Enum.map(&String.length/1)
      |> Enum.map(&(&1 + 2))
      |> Enum.sum()

    {one, two, two - one, three, three - two}
  end

  def clean(string) do
    step0 = Regex.replace(~r/\\\\/, string, "_")
    step1 = Regex.replace(~r/\\x\w{2}/, step0, "_")
    Regex.replace(~r/\\\"/, step1, "_")
  end

  def unclean(string) do
    step0 = Regex.replace(~r<\\>, string, "\\\\\\")
    Regex.replace(~r/"/, step0, "\\\"")
  end

  def solve(file) do
    file
    |> File.read!()
    |> compute()
  end
end

# 1248 -> too low
# 1356 -> too high
Space.solve("day8.txt")
|> IO.inspect()

# 870 -> too low
# 1470 -> too low
