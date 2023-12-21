defmodule Day21 do
  def main do
    p1()
  end

  def p1() do
    grid = read()
    start = Enum.find(grid, fn {{_x, _y}, v} -> v == "S" end) |> elem(0)
    queue = :queue.from_list([{start, 0}])
    seen = MapSet.new([start])
    maxsteps = 50
    griddimx = Enum.max_by(grid, fn {{x, _}, _} -> x end) |> elem(0) |> elem(0)
    griddimy = Enum.max_by(grid, fn {{_, y}, _} -> y end) |> elem(0) |> elem(1)

    run(queue, grid, seen, maxsteps, MapSet.new(), rescale(griddimx, griddimy))
    |> MapSet.size()
  end

  def run(queue, grid, seen, maxsteps, res, rescale_func) do
    {{:value, {{x, y}, steps}}, queue} = :queue.out(queue)

    if steps == maxsteps do
      res = MapSet.new(:queue.to_list(queue))
      MapSet.put(res, {x, y})
    else
      candidates =
        [{x + 1, y}, {x - 1, y}, {x, y + 1}, {x, y - 1}]
        |> Enum.filter(fn {i, j} ->
          {newx, newy} = rescale_func.({i, j})

          grid[{newx, newy}] != "#" and
            not MapSet.member?(seen, {i, j, steps + 1})
        end)

      seen =
        Enum.reduce(candidates, seen, fn {x, y}, seen ->
          MapSet.put(seen, {x, y, steps + 1})
        end)

      queue =
        Enum.reduce(candidates, queue, fn c, q ->
          :queue.in({c, steps + 1}, q)
        end)

      run(queue, grid, seen, maxsteps, res, rescale_func)
    end
  end

  def rescale(griddimx, griddimy) do
    fn {i, j} ->
      newx =
        if i >= 0 do
          rem(i, griddimx + 1)
        else
          griddimx - rem(abs(i), griddimx + 1) + 1
        end

      newy =
        if j >= 0 do
          rem(j, griddimy + 1)
        else
          griddimy - rem(-j, griddimy + 1) + 1
        end

      {newx, newy}
    end
  end

  def read() do
    File.stream!("data/day21_test.txt")
    |> Enum.map(fn line ->
      line
      |> String.trim()
      |> String.split("", trim: true)
      |> Enum.with_index()
    end)
    |> Enum.with_index()
    |> Enum.map(fn {row, y} ->
      Enum.map(row, fn {v, x} -> {{x, y}, v} end)
    end)
    |> Enum.concat()
    |> Enum.into(%{})
  end
end
