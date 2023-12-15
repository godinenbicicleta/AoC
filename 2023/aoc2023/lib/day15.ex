defmodule Day15 do
  def main do
    labels =
      File.read!("data/day15.txt")
      |> String.trim()
      |> String.split(",")

    labels
    |> Enum.reduce(0, &(&2 + hash(&1)))
    |> IO.inspect(label: "p1")

    boxes =
      Enum.into(0..255, %{}, &{&1, []})

    Enum.reduce(labels, boxes, &reducer/2)
    |> Enum.reduce(0, fn {box_id, vals}, total ->
      Stream.with_index(vals, 1)
      |> Enum.reduce(total, fn {{_name, val}, ix}, acc -> acc + val * ix * (box_id + 1) end)
    end)
    |> IO.inspect(label: "p2")
  end

  def reducer(label, boxes) do
    if String.contains?(label, "=") do
      [name, num] = String.split(label, "=")
      num = String.to_integer(num)
      ix = hash(name)
      box = boxes[ix]
      box = update(box, {name, num})
      Map.put(boxes, ix, box)
    else
      [name] = String.split(label, "-", trim: true)
      ix = hash(name)

      box =
        boxes[ix]
        |> remove(name)

      Map.put(boxes, ix, box)
    end
  end

  def remove([], _), do: []
  def remove([{name, _} | rest], name), do: rest
  def remove([h | t], name), do: [h | remove(t, name)]

  def update([], p), do: [p]
  def update([{name, _} | rest], p = {name, _}), do: [p | rest]
  def update([head | rest], p), do: [head | update(rest, p)]

  def hash(s) do
    s
    |> String.to_charlist()
    |> hash(0)
  end

  def hash([], value), do: value

  def hash([char | rest], value) do
    value
    |> Kernel.+(char)
    |> Kernel.*(17)
    |> rem(256)
    |> then(&hash(rest, &1))
  end
end
