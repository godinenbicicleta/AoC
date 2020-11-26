defmodule Container do
  def container_map(:test) do
    %{1 => 20, 2 => 15, 3 => 10, 4 => 5, 5 => 5}
  end

  def container_map(_) do
    Enum.with_index([11, 30, 47, 31, 32, 36, 3, 1, 5, 3, 32, 36, 15, 11, 46, 26, 28, 1, 19, 3])
    |> Enum.into(%{}, fn {x, y} -> {y, x} end)
  end

  def solve(liters, env) do
    containers = container_map(env)

    goal =
      if env == :test do
        25
      else
        150
      end

    make(liters, containers, [], goal)
    |> flatten
    |> Enum.reduce([], fn x, acc -> to_map(x, acc) end)
    |> Enum.uniq()
    |> Enum.filter(fn x -> Enum.sum(Map.values(x)) == goal end)
  end

  def to_map(l = [y | _], acc) when is_list(y) do
    Enum.map(l, fn x -> Enum.into(x, %{}) end) ++ acc
  end

  def to_map(x, acc) do
    [Enum.into(x, %{}) | acc]
  end

  def flatten([]) do
    []
  end

  def flatten(list = [[smth | _] | _]) when not is_list(smth) do
    list
  end

  def flatten(list = [[smth | _] | tail]) when is_list(smth) do
    flatten(hd(list)) ++ flatten(tail)
  end

  def flatten(lol = [[] | t]) when is_list(t) do
    flatten(t)
  end

  def make(n, [], res, goal) do
    res
  end

  def make(n, _containers, res, goal) when n < 5 do
    res
  end

  def make(n, containers, [], goal) do
    possible = Enum.filter(containers, fn {_, x} -> x <= n end) |> Enum.into(%{})

    for {key, p} <- possible do
      new_possible = Map.delete(possible, key)

      make(n - p, new_possible, [{key, p}], goal)
    end
  end

  def make(n, containers, res, goal) do
    possible = Enum.filter(containers, fn {_, x} -> x <= n end) |> Enum.into(%{})

    if map_size(possible) > 0 do
      for {key, p} <- possible, test(res, {key, p}, goal) do
        new_possible = Map.delete(possible, key)

        make(n - p, new_possible, [{key, p} | res], goal)
      end
    else
      res
    end
  end

  def test(res, {key, p}, goal) do
    (res |> Enum.map(fn {key, v} -> v end) |> Enum.sum()) + p <= goal
  end
end

Container.solve(25, :test)
|> IO.inspect()

Container.solve(150, :prod)
|> IO.inspect()
