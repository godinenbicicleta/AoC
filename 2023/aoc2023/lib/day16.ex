defmodule Day16 do
  def main do
    grid = read()
    current = {0, 0, :east}
    seen = MapSet.new([current])

    queue = [current]

    {_grid, seen} = run(queue, grid, seen)
    seen |> Enum.map(fn {x, y, _dir} -> {x, y} end) |> Enum.uniq() |> Enum.count()
  end

  def run([], grid, seen), do: {grid, seen}

  def run([h | t], grid, seen) do
    seen = MapSet.put(seen, h)

    next_positions =
      next(h, grid)
      |> Enum.filter(fn x -> not MapSet.member?(seen, x) end)

    run(next_positions ++ t, grid, seen)
  end

  def next({x, y, dir}, grid) do
    new_pos =
      {newx, newy} =
      case dir do
        :north -> {x, y - 1}
        :south -> {x, y + 1}
        :east -> {x + 1, y}
        :west -> {x - 1, y}
      end

    next_value = grid[new_pos]

    case next_value do
      nil ->
        []

      "." ->
        [{newx, newy, dir}]

      "/" ->
        case dir do
          :east -> [{newx, newy, :north}]
          :west -> [{newx, newy, :south}]
          :south -> [{newx, newy, :west}]
          :north -> [{newx, newy, :east}]
        end

      "\\" ->
        case dir do
          :east -> [{newx, newy, :south}]
          :west -> [{newx, newy, :north}]
          :south -> [{newx, newy, :east}]
          :north -> [{newx, newy, :west}]
        end

      "-" ->
        case dir do
          :east -> [{newx, newy, :east}]
          :west -> [{newx, newy, :west}]
          :south -> [{newx, newy, :west}, {newx, newy, :east}]
          :north -> [{newx, newy, :west}, {newx, newy, :east}]
        end

      "|" ->
        case dir do
          :east -> [{newx, newy, :south}, {newx, newy, :north}]
          :west -> [{newx, newy, :south}, {newx, newy, :north}]
          :south -> [{newx, newy, :south}]
          :north -> [{newx, newy, :north}]
        end
    end
  end

  def read() do
    File.stream!("data/day16.txt")
    |> Enum.map(fn line ->
      line
      |> String.trim()
      |> String.split("", trim: true)
      |> Enum.with_index()
    end)
    |> Enum.with_index()
    |> Enum.map(fn {row, y} ->
      Enum.map(row, fn {c, x} ->
        {{x, y}, c}
      end)
    end)
    |> Enum.concat()
    |> Enum.into(%{})
  end
end
