defmodule Day3 do
  def get_contents do
    File.read!("day3.txt")
    |> String.trim()
    |> String.split("\n", trim: true)
    |> Stream.map(fn row -> String.graphemes(row) |> Enum.with_index() end)
    |> Stream.with_index()
    |> Enum.reduce(
      %{},
      fn {row, index}, acc ->
        Enum.into(row, acc, fn {char, ix} -> {{ix, index}, char} end)
      end
    )
  end

  def run(right, down) do
    contents = get_contents()

    {{_, height}, _} = Enum.max_by(contents, fn {{_x, y}, _char} -> y end)
    {{width, _}, _} = Enum.max_by(contents, fn {{x, _y}, _char} -> x end)
    trees = 0
    start = {0, 0}
    move(start, contents, height + 1, width + 1, trees, right, down)
  end

  def move({_, y}, _, height, _width, trees, _right, down) when y + down > height do
    trees
  end

  def move({x, y}, contents, height, width, trees, right, down) do
    next_pos = {rem(x + right, width), y + down}

    if contents[next_pos] == "#" do
      move(next_pos, contents, height, width, trees + 1, right, down)
    else
      move(next_pos, contents, height, width, trees, right, down)
    end
  end
end

Day3.run(3, 1)
|> IO.inspect()

[{1, 1}, {3, 1}, {5, 1}, {7, 1}, {1, 2}]
|> Enum.map(fn {r, d} -> Day3.run(r, d) end)
|> Enum.reduce(1, &Kernel.*/2)
|> IO.inspect()
