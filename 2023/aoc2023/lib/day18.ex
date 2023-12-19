defmodule Day18 do
  def main do
    p1() |> IO.inspect()
    p2() |> IO.inspect()
  end

  def get_border(lines) do
    lines
    |> Enum.reduce({MapSet.new([{0, 0}]), {0, 0}}, fn {dir, steps}, {seen, {x, y}} ->
      case dir do
        "R" ->
          seen =
            Enum.reduce(1..steps, seen, fn step, seen ->
              MapSet.put(seen, {x + step, y})
            end)

          {seen, {x + steps, y}}

        "D" ->
          seen =
            Enum.reduce(1..steps, seen, fn step, seen ->
              MapSet.put(seen, {x, y + step})
            end)

          {seen, {x, y + steps}}

        "L" ->
          seen =
            Enum.reduce(1..steps, seen, fn step, seen ->
              MapSet.put(seen, {x - step, y})
            end)

          {seen, {x - steps, y}}

        "U" ->
          seen =
            Enum.reduce(1..steps, seen, fn step, seen ->
              MapSet.put(seen, {x, y - step})
            end)

          {seen, {x, y - steps}}
      end
    end)
    |> elem(0)
  end

  def insert(elem, []) do
    [elem]
  end

  def insert({new_start, new_end}, [{old_start, old_end} | rest]) do
    cond do
      new_end < old_start - 1 ->
        [{new_start, new_end}, {old_start, old_end} | rest]

      new_start > old_end + 1 ->
        [{old_start, old_end} | insert({new_start, new_end}, rest)]

      true ->
        [{min(new_start, old_start), max(new_end, old_end)} | rest]
    end
  end

  def get_border2(lines) do
    lines
    |> Enum.reduce({Map.new([{0, [{0, 0}]}]), {0, 0}}, fn {dir, steps}, {seen, {x, y}} ->
      case dir do
        "R" ->
          seen =
            Map.update(seen, y, [{x + 1, x + steps}], fn existing ->
              insert({x + 1, x + steps}, existing)
            end)

          {seen, {x + steps, y}}

        "D" ->
          seen =
            Enum.reduce(1..steps, seen, fn step, seen ->
              Map.update(seen, y + step, [{x, x}], fn existing -> insert({x, x}, existing) end)
            end)

          {seen, {x, y + steps}}

        "L" ->
          seen =
            Map.update(seen, y, [{x - steps, x - 1}], fn existing ->
              insert({x - steps, x - 1}, existing)
            end)

          {seen, {x - steps, y}}

        "U" ->
          seen =
            Enum.reduce(1..steps, seen, fn step, seen ->
              Map.update(seen, y - step, [{x, x}], fn existing -> insert({x, x}, existing) end)
            end)

          {seen, {x, y - steps}}
      end
    end)
    |> elem(0)
  end

  def p1 do
    border = get_border(read1())

    # render(border)
    seed = find_seed(border)

    seen = run([seed], border, MapSet.new())

    MapSet.size(seen) + MapSet.size(border)
  end

  def find(bordermap, key, value) do
    bordermap[key] != nil and
      Enum.find(bordermap[key], fn {s, e} -> s == value and e == value end) != nil
  end

  def reducer({y, intervals}, {bordermap, acc}) do
    {_in_out, _prev, ytotal} =
      Enum.reduce(intervals, {:outside, nil, acc}, fn
        {start, end_}, {:inside, {_prev_start, prev_end}, acc2} ->
          if start == end_ do
            {:outside, {start, end_}, acc2 + start - prev_end}
          else
            new_acc = acc2 + start - prev_end - 1 + end_ - start + 1

            find_start_above = find(bordermap, y - 1, start)
            find_start_below = find(bordermap, y + 1, start)
            find_end_above = find(bordermap, y - 1, end_)
            find_end_below = find(bordermap, y + 1, end_)

            case {find_start_above, find_end_above, find_start_below, find_end_below} do
              {true, true, _, _} ->
                {:inside, {start, end_}, new_acc}

              {_, _, true, true} ->
                {:inside, {start, end_}, new_acc}

              _ ->
                {:outside, {start, end_}, new_acc}
            end
          end

        {start, end_}, {:outside, _prev, acc2} ->
          if start == end_ do
            {:inside, {start, end_}, acc2 + 1}
          else
            new_acc = acc2 + end_ - start + 1
            find_start_above = find(bordermap, y - 1, start)
            find_start_below = find(bordermap, y + 1, start)
            find_end_above = find(bordermap, y - 1, end_)
            find_end_below = find(bordermap, y + 1, end_)

            case {find_start_above, find_end_above, find_start_below, find_end_below} do
              {true, true, _, _} ->
                {:outside, {start, end_}, new_acc}

              {_, _, true, true} ->
                {:outside, {start, end_}, new_acc}

              _ ->
                {:inside, {start, end_}, new_acc}
            end
          end
      end)

    {bordermap, ytotal}
  end

  def p2 do
    bordermap = get_border2(read2())

    bordermap
    |> Enum.reduce({bordermap, 0}, &reducer/2)
    |> elem(1)
  end

  def run([], _border, seen), do: seen

  def run([{x, y} | rest], border, seen) do
    candidates = [
      {x + 1, y},
      {x - 1, y},
      {x, y + 1},
      {x, y - 1}
    ]

    {rest, seen} =
      Enum.reduce(candidates, {rest, seen}, fn c, {rest, seen} ->
        if MapSet.member?(seen, c) or MapSet.member?(border, c) do
          {rest, seen}
        else
          {[c | rest], MapSet.put(seen, c)}
        end
      end)

    run(rest, border, seen)
  end

  def find_seed(seen) do
    {x, y} = seen |> Enum.sort() |> hd
    {x + 1, y + 1}
  end

  def render(seen) do
    %{maxx: maxx, minx: minx, maxy: maxy, miny: miny} = dimensions(seen)

    for y <- miny..maxy do
      for x <- minx..maxx do
        if MapSet.member?(seen, {x, y}), do: "#", else: "."
      end
      |> Enum.join()
    end
    |> Enum.join("\n")
    |> IO.puts()
  end

  def dimensions(seen) do
    {{minx, _}, {maxx, _}} = Enum.min_max_by(seen, fn {x, _y} -> x end)
    {{_, miny}, {_, maxy}} = Enum.min_max_by(seen, fn {_x, y} -> y end)
    %{maxx: maxx, minx: minx, maxy: maxy, miny: miny}
  end

  def read1() do
    File.stream!("data/day18.txt")
    |> Enum.map(fn line ->
      line
      |> String.trim()
      |> String.split()
    end)
    |> Enum.map(fn [dir, steps, _rgb] -> {dir, String.to_integer(steps)} end)
  end

  def read2() do
    File.stream!("data/day18.txt")
    |> Enum.map(fn line ->
      line
      |> String.trim()
      |> String.split()
    end)
    |> Enum.map(fn [_dir, _steps, rgb] ->
      distance = String.slice(rgb, 2, 5) |> String.to_integer(16)
      direction = String.slice(rgb, 7, 1) |> to_dir()
      {direction, distance}
    end)
  end

  def to_dir("0"), do: "R"
  def to_dir("2"), do: "L"
  def to_dir("1"), do: "D"
  def to_dir("3"), do: "U"
end
