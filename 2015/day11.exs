defmodule Password do
  def next(password) do
    new =
      password
      |> String.reverse()
      |> String.to_charlist()
      |> increment

    if is_valid?(new) do
      new |> List.to_string()
    else
      new |> List.to_string() |> next
    end
  end

  def is_valid?(charlist) do
    rule1?(charlist) and rule2?(charlist) and rule3?(charlist)
  end

  def rule3?(charlist) do
    not Enum.any?(charlist, fn char -> char == ?i or char == ?l or char == ?o end)
  end

  def rule2?(charlist) do
    res =
      charlist
      |> Enum.chunk_while([], &at_least_2/2, &after_at_least_2/1)
      |> Enum.filter(fn x -> length(x) > 1 end)

    length(res) > 1
  end

  def at_least_2(char, []) do
    {:cont, [char]}
  end

  def at_least_2(head, acc = [head]) do
    {:cont, [head | acc], []}
  end

  def at_least_2(char, acc) do
    {:cont, acc, [char]}
  end

  def after_at_least_2(res) do
    {:cont, res}
  end

  def rule1?(charlist) do
    charlist
    |> Enum.chunk_while([], &chunk_fun/2, &after_fun/1)
    |> Enum.filter(fn x -> length(x) > 2 end)
    |> Enum.any?()
  end

  def chunk_fun(char, []) do
    {:cont, [char]}
  end

  def chunk_fun(char, acc = [head | _]) do
    if char - 1 == head do
      {:cont, [char | acc]}
    else
      {:cont, acc, [char]}
    end
  end

  def after_fun(res) do
    {:cont, res}
  end

  def increment(charlist) do
    charlist
    |> Enum.reduce([], &reducer/2)
    |> Enum.map(&elem(&1, 0))
  end

  def reducer(char, []) do
    if char != ?z do
      [{add(char), :cont}]
    else
      [{?a, :inc}]
    end
  end

  def reducer(char, acc = [{_, :cont} | _]) do
    [{char, :cont} | acc]
  end

  def reducer(char, acc = [{_, :inc} | _]) do
    if char != ?z do
      [{add(char), :cont} | acc]
    else
      [{?a, :inc} | acc]
    end
  end

  def add(?h) do
    ?h + 2
  end

  def add(?n) do
    ?n + 2
  end

  def add(?k) do
    ?k + 2
  end

  def add(char) do
    char + 1
  end
end

# abcdefgh => abcdffaa
# ghijklmn => ghjaabcc
#
Password.next("vzbxkghb") |> IO.inspect()
