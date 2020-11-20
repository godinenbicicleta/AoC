contents = File.read!("day1.txt")

contents
|> String.trim()
|> String.split("", trim: true)
|> Enum.reduce(0, fn
  "(", acc -> acc + 1
  ")", acc -> acc - 1
end)
|> IO.puts()

reducer = fn
  {_, index}, -1 -> {:halt, index}
  {"(", _}, acc -> {:cont, acc + 1}
  {")", _}, acc -> {:cont, acc - 1}
end

contents
|> String.trim()
|> String.split("", trim: true)
|> Enum.with_index()
|> Enum.reduce_while(0, reducer)
|> IO.puts()
