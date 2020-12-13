defmodule Day12 do
  def run do
    {{x1, y1, _}, {{x2, y2}, {_, _}}} =
      File.stream!("day12.txt")
      |> Enum.map(&parse/1)
      |> run()

    IO.puts("p1: #{abs(x1) + abs(y1)}")
    IO.puts("p2: #{abs(x2) + abs(y2)}")
  end

  def run(list) do
    s = {0, 0, "E"}
    sw = {{0, 0}, {10, 1}}
    p1 = Enum.reduce(list, s, &move1/2)
    p2 = Enum.reduce(list, sw, &move2/2)
    {p1, p2}
  end

  def move2(instruction, {s, w}), do: mv2(instruction, {s, w}) |> IO.inspect()

  def mv2({"N", num}, {s, {x, y}}), do: {s, {x, y + num}}
  def mv2({"S", num}, {s, {x, y}}), do: {s, {x, y - num}}
  def mv2({"E", num}, {s, {x, y}}), do: {s, {x + num, y}}
  def mv2({"W", num}, {s, {x, y}}), do: {s, {x - num, y}}
  def mv2({"F", num}, {{x, y}, w = {wx, wy}}), do: {{x + num * wx, y + num * wy}, w}
  def mv2({"L", num}, {s, w}), do: {s, rotate(w, num)}
  def mv2({"R", num}, {s, w}), do: {s, rotate(w, 360 - num)}

  def rotate({x, y}, deg) do
    r = :math.sqrt(x * x + y * y)
    theta = :math.atan2(y, x) + :math.pi() / 180 * deg
    x = round(r * :math.cos(theta))
    y = round(r * :math.cos(theta))
    {x, y}
  end

  def move1(a, b), do: mv(a, b) |> IO.inspect()

  def mv({"F", num}, {x, y, "N"}), do: {x, y + num, "N"}
  def mv({"F", num}, {x, y, "S"}), do: {x, y - num, "S"}
  def mv({"F", num}, {x, y, "E"}), do: {x + num, y, "E"}
  def mv({"F", num}, {x, y, "W"}), do: {x - num, y, "W"}
  def mv({"N", num}, {x, y, f}), do: {x, y + num, f}
  def mv({"S", num}, {x, y, f}), do: {x, y - num, f}
  def mv({"E", num}, {x, y, f}), do: {x + num, y, f}
  def mv({"W", num}, {x, y, f}), do: {x - num, y, f}
  def mv({"L", deg}, {x, y, f}), do: {x, y, turn(f, rem(deg, 360))}
  def mv({"R", deg}, {x, y, f}), do: {x, y, turn(f, 360 - rem(deg, 360))}

  @m1 %{"N" => 90, "E" => 0, "W" => 180, "S" => 270}
  @m2 %{90 => "N", 0 => "E", 180 => "W", 270 => "S"}
  def turn(f, deg), do: @m2[rem(@m1[f] + deg, 360)]

  def parse(string) do
    {str, num} =
      string
      |> String.trim()
      |> String.split_at(1)

    {str, String.to_integer(num)}
  end
end
