defmodule Day12 do
  def read do
    {x, y, _} =
      File.read!("day12.txt")
      |> String.trim()
      |> String.split("\n", trim: true)
      |> Enum.map(&parse/1)
      |> Enum.reduce({0, 0, "E"}, &move/2)

    IO.puts("p1: #{abs(x) + abs(y)}")
  end

  def parse(string) do
    {str, num} = String.split_at(string, 1)
    {str, String.to_integer(num)}
  end

  def move(a, b), do: mv(a, b) |> IO.inspect()

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
end
