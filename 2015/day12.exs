defmodule Json do
  def read(file) do
    File.read!(file)
  end
end

Regex.scan(~r/(-?\d+)/, Json.read("day12.txt"))
|> Enum.map(fn [x, _] -> elem(Integer.parse(x), 0) end)
|> Enum.sum()
|> IO.inspect()

# 119433
