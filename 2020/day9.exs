defmodule Day9 do
  def read(file) do
    file
    |> File.stream!()
    |> Stream.with_index()
    |> Enum.map(&parse/1)
  end

  def parse({str, ix}), do: {String.to_integer(String.trim(str)), ix}

  def locate(target), do: locate(target, read("day9.txt"))

  def locate(target, nums), do: locate(target, nums, :queue.new(), 0)

  def locate(target, _, q, target) do
    {min, max} =
      :queue.to_list(q)
      |> Enum.min_max()

    min + max
  end

  def locate(target, [{h, _ix} | t], q, total) when total < target do
    q = :queue.in(h, q)
    locate(target, t, q, total + h)
  end

  def locate(target, [{h, _ix} | t], q, total) do
    {q, total} = drop_while(q, total, target)
    q = :queue.in(h, q)
    locate(target, t, q, total + h)
  end

  def drop_while(q, total, target) when total > target do
    {{:value, val}, q} = :queue.out(q)
    drop_while(q, total - val, target)
  end

  def drop_while(q, total, _target), do: {q, total}

  def run(nums, 1), do: run(nums, MapSet.new(), %{})

  def run([{h, pos} | t], prev, positions) when pos < 25 do
    run(t, MapSet.put(prev, h), Map.put(positions, pos, h))
  end

  def run([{h, pos} | t], prev, positions) do
    case sum(prev, h) do
      {_num1, _num2} ->
        to_drop = Map.get(positions, pos - 25)

        prev =
          if to_drop do
            MapSet.delete(prev, to_drop)
          else
            prev
          end

        run(t, MapSet.put(prev, h), Map.put(positions, pos, h))

      _ ->
        h
    end
  end

  def sum(prev, h) do
    res =
      for x <- prev, y <- prev, x != y and x + y == h do
        {x, y}
      end

    if res == [], do: res, else: hd(res)
  end
end

Day9.read("day9.txt")
|> Day9.run(1)
|> IO.inspect()
|> Day9.locate()
|> IO.inspect()
