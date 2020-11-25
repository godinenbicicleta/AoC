defmodule One do
  def run(input, 0) do
    input
  end

  def run(input, n) do
    run(input)
    |> run(n - 1)
  end

  def run(input) do
    input
    |> String.graphemes()
    |> Enum.chunk_while([], &chunk_fun/2, &after_fun/1)
    |> Enum.join("")
  end

  def chunk_fun(element, []) do
    {:cont, [element]}
  end

  def chunk_fun(element, acc = [element | _]) do
    {:cont, [element | acc]}
  end

  def chunk_fun(element, acc = [h | _]) do
    {:cont, "#{length(acc)}#{h}", [element]}
  end

  def after_fun([]) do
    {:cont, []}
  end

  def after_fun(acc = [h | _]) do
    {:cont, "#{length(acc)}#{h}", []}
  end
end

One.run("111221", 1)
# expected = 312211
|> IO.inspect()

One.run("1113222113", 40)
|> String.length()
|> IO.inspect()

One.run("1113222113", 50)
|> String.length()
|> IO.inspect()
